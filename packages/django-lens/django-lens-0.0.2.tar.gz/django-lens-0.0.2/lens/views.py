# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers


from .models import Trace, TraceSetting


def last_trace_entry(request):
    try:
        return Trace.objects.filter(type="request").latest().modified
    except:
        return timezone.now()


def trace_last_modified(request, **kwargs):
    try:
        return Trace.objects.get(**kwargs).modified
    except:
        return timezone.now()
    
cache_decorators = [vary_on_headers('Cookie', 'HX-Request'), cache_control(max_age=60 * 60 * 24)]

@method_decorator([last_modified(last_trace_entry), *cache_decorators], name='dispatch')
class RequestListView(ListView):
    queryset = Trace.objects.filter(type="request")
    context_object_name = "traces"
    paginate_by = 20

    def get_template_names(self):
        if 'hx-request' in self.request.headers:
            return ["lens/components/trace_list.html"]
        return ["lens/list.html"]

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, trace_setting=TraceSetting.get(), **kwargs)


@method_decorator([last_modified(trace_last_modified), *cache_decorators], name='dispatch')
class RequestDetailView(DetailView):
    queryset = Trace.objects.filter(type="request")
    slug_field = "request_id"
    context_object_name = "trace"
    slug_url_kwarg = "request_id"

    def get_template_names(self):
        if 'hx-request' in self.request.headers:
            return ["lens/panels/request.html"]
        return ["lens/detail.html"]
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "tabs": [
                {"name": "response", "label": "Response"},
                {"name": "payload", "label": "Payload"},
                {"name": "request_headers", "label": "Request Headers"},
                {"name": "response_headers", "label": "Response Headers"},
                {"name": "sql_queries", "label": "SQL Queries"},
                {"name": "print_log", "label": "Print Log"},
                {"name": "http_requests", "label": "HTTP Requests"},
            ]
        })
        return ctx

@method_decorator([last_modified(trace_last_modified), *cache_decorators], name='dispatch')
class TraceDetailView(DetailView):
    queryset = Trace.objects.all()
    context_object_name = "trace"

    def get_template_names(self):
        if self.object.type == 'client_request':
            return ["lens/panels/client_request.html"]
        elif self.object.type == 'sql':
            return ["lens/panels/sql.html"]
        return ["lens/panels/request.html"]
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        tabs = {
            "request": [],
            "client_request": [
                {"name": "response", "label": "Response"},
                {"name": "payload", "label": "Payload"},
                {"name": "request_headers", "label": "Request Headers"},
                {"name": "response_headers", "label": "Response Headers"},
            ],
            "sql": [
                {"name": "sql", "label": "SQL"},
                {"name": "stacktrace", "label": "Stacktrace"},
            ],
            "print": [],
        }

        current_tabs = tabs[self.object.type]

        if self.object.type == 'client_request':
            if self.object.data.get("status_code") == -1:
                current_tabs.append({"name": "error", "label": "Error"})

        ctx.update({"tabs": current_tabs})
        return ctx


class SettingsView(TemplateView):
    template_name = "lens/settings.html"

    def get_context_data(self, **kwargs):
        kwargs.update({"trace_setting": TraceSetting.get()})
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        trace_setting = TraceSetting.get()

        if "enabled" in request.POST:
            trace_setting.enabled = request.POST.get("enabled", "yes") == "yes"

        if "stacktrace_enabled" in request.POST:
            trace_setting.stacktrace_enabled = request.POST.get("stacktrace_enabled", "yes") == "yes"

        trace_setting.save()
        return redirect("lens:settings")


def delete_trace(request, request_id):
    if request.method == "POST":
        if request_id == "all":
            Trace.objects.all().delete()
        else:
            Trace.objects.filter(request_id=request_id).delete()
    return redirect("lens:trace_list")
