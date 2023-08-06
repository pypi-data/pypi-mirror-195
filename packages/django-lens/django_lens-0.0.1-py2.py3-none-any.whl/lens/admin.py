# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Trace, TraceSetting


@admin.register(Trace)
class TraceAdmin(admin.ModelAdmin):
    pass


@admin.register(TraceSetting)
class TraceSettingAdmin(admin.ModelAdmin):
    pass
