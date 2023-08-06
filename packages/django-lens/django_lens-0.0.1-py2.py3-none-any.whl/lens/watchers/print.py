import builtins
from functools import partial
from pprint import pformat

from django.utils import timezone

from lens import traces

from ..models import Trace
from .base import Watcher


class PrintWatcher(Watcher):
    def install(self):
        builtins._original_print = builtins.print
        builtins.print = partial(print_wrapper, self.lens)

    def uninstall(self):
        if hasattr(builtins, "_original_print"):
            builtins.print = builtins._original_print
            del builtins._original_print


def print_wrapper(lens, *objects, **kwargs):
    trace = {"start_time": timezone.now(), "value": "".join((str(obj) for obj in objects))}
    retval = builtins._original_print(*objects, **kwargs)
    trace["end_time"] = timezone.now()
    traces.add(
        Trace(
            type="print",
            request_id=lens.request_id,
            start_time=trace["start_time"],
            end_time=trace["end_time"],
            data=trace,
        )
    )
    return retval
