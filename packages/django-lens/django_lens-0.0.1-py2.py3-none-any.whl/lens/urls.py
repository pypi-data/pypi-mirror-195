# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views

app_name = "lens"
urlpatterns = [
    re_path(
        route="^$",
        view=views.RequestListView.as_view(),
        name="trace_list",
    ),
    re_path(
        route="^settings/$",
        view=views.SettingsView.as_view(),
        name="settings",
    ),
    re_path(
        route="^(?P<request_id>[\w-]+)/$",
        view=views.RequestDetailView.as_view(),
        name="trace_detail",
    ),
    re_path(
        route="^traces/(?P<pk>[\d]+)/$",
        view=views.TraceDetailView.as_view(),
        name="trace_panel",
    ),
    re_path(
        route="^(?P<request_id>[\w-]+)/delete/$",
        view=views.delete_trace,
        name="delete_trace",
    ),
]
