# -*- coding: utf-8 -*-
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from jsonfield import JSONField
from model_utils.models import TimeStampedModel


class Trace(TimeStampedModel):
    TYPE_CHOICES = (
        ("request", "Request"),
        ("sql", "SQL Query"),
        ("print", "Print Calls"),
        ("client_request", "Client Requests"),
    )
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, db_index=True)
    request_id = models.UUIDField(db_index=True)
    data = JSONField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.request_id} - {self.type}"

    def sql_traces(self):
        return self.child_traces("sql")

    def print_traces(self):
        return self.child_traces("print")

    def print_trace_values(self):
        return "\n".join((trace_data.get("value", "") for trace_data in self.child_traces("print").values_list("data", flat=True)))

    def client_request_traces(self):
        return self.child_traces("client_request")

    def child_traces(self, type):
        return Trace.objects.filter(request_id=self.request_id, type=type).reverse()

    @property
    def duration_milliseconds(self):
        return self.duration * 1_000

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()


class TraceSetting(TimeStampedModel):
    enabled = models.BooleanField(default=True)
    stacktrace_enabled = models.BooleanField(default=False)

    @classmethod
    def get(cls):
        return cls.objects.get_or_create()[0]


class Lens:
    def __init__(self, request_id=None):
        self.request_id = request_id or str(uuid.uuid4())
        self.trace_setting = TraceSetting.get()

    def should_process(self, request):
        if not self.trace_setting.enabled:
            return False

        for path_prefix in getattr(
            settings, "LENS_EXCLUDE_PATH_PREFIXES", [reverse("lens:trace_list")]
        ):
            if request.path.startswith(path_prefix):
                return False

        return True
