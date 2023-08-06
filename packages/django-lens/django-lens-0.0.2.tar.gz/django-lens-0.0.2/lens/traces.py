from collections import defaultdict
from threading import local

_tracer_context = local()


def get_tracer_context():
    if not hasattr(_tracer_context, "traces"):
        _tracer_context.traces = defaultdict(list)
    return _tracer_context


def add(trace):
    tracer_context = get_tracer_context()
    tracer_context.traces[trace.request_id].append(trace)


def collect(request_id):
    tracer_context = get_tracer_context()
    return tracer_context.traces.pop(request_id)
