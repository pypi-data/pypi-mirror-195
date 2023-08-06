from django.utils import timezone

from lens import traces

from ..models import Trace
from .base import Watcher


class RequestWatcher(Watcher):
    def process_request(self, request):
        """
        Initialize a trace and inject Request ID HTTP header in request.
        """
        self.trace = Trace(
            type="request", request_id=self.lens.request_id, start_time=timezone.now()
        )

    def process_response(self, request, response):
        """
        Collect trace data and inject Request ID HTTP header in response.
        """
        response["X-Lens-Request-Id"] = self.lens.request_id
        self.trace.data = {
            "path": request.get_full_path(),
            "method": request.method,
            "status_code": response.status_code,
            "host": request.headers["host"],
            "remote_addr": request.META["REMOTE_ADDR"],
            "content_type": request.content_type,
            "query_string": request.GET.urlencode(),
            "query_params": request.GET.dict(),
            "form_data": request.POST.dict(),
            "request_data": request.body,
            "request_headers": request.headers,
            "cookies": request.COOKIES,
            "response_headers": response.headers,
            "response_data": "Streaming Response"
            if response.streaming
            else response.content,
        }
        self.trace.end_time = timezone.now()
        traces.add(self.trace)
