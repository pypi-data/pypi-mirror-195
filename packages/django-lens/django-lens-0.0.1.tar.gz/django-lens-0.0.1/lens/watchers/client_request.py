import traceback

import requests
from django.utils import timezone

from .. import traces
from ..models import Trace
from .base import Watcher


class ClientRequestWatcher(Watcher):
    def install(self):
        requests.adapters.HTTPAdapter._original_send = (
            requests.adapters.HTTPAdapter.send
        )

        def send_wrapper(adapter, request, stream=False, *args, **kwargs):
            trace = {
                "start_time": timezone.now(),
                "url": request.url,
                "method": request.method,
                "request_headers": request.headers,
                "request_data": "Streaming" if stream else request.body,
            }
            try:
                response = adapter._original_send(request, *args, **kwargs)
            except:
                trace.update(
                    {
                        "response_headers": {},
                        "status_code": -1,
                        "exc_info": traceback.format_exc(),
                        "response_data": None,
                        "end_time": timezone.now(),
                    }
                )
                raise
            else:
                trace.update(
                    {
                        "response_headers": response.headers,
                        "status_code": response.status_code,
                        "response_data": "Streaming" if stream else response.content,
                        "end_time": timezone.now(),
                    }
                )
            finally:
                traces.add(
                    Trace(
                        request_id=self.lens.request_id,
                        type="client_request",
                        start_time=trace["start_time"],
                        end_time=trace["end_time"],
                        data=trace,
                    )
                )
            return response

        requests.adapters.HTTPAdapter.send = send_wrapper

    def uninstall(self):
        if hasattr(requests.adapters.HTTPAdapter, "_original_send"):
            requests.adapters.HTTPAdapter.send = (
                requests.adapters.HTTPAdapter._original_send
            )
            del requests.adapters.HTTPAdapter._original_send
