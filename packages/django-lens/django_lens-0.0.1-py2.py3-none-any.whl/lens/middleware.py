from lens import traces

from .models import Lens, Trace
from .watchers import (ClientRequestWatcher, PrintWatcher, RequestWatcher,
                       SQLWatcher)


class LensMiddleware:
    watcher_classes = [RequestWatcher, SQLWatcher, PrintWatcher, ClientRequestWatcher]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.lens = Lens(request.META.get("HTTP_X_REQUEST_ID"))
        if not self.lens.should_process(request):
            return self.get_response(request)

        watchers = []
        for watcher_cls in self.watcher_classes:
            watcher = watcher_cls(self.lens)
            watcher.install()
            watchers.append(watcher)

        # process request through watcher
        for watcher in watchers:
            watcher.process_request(request)

        # run the view
        response = self.get_response(request)

        for watcher in watchers:
            watcher.process_response(request, response)
            watcher.uninstall()

        Trace.objects.bulk_create(traces.collect(self.lens.request_id))
        return response
