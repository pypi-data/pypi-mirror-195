class Watcher:
    """
    Base implementation which defines the API for watchers.
    """

    def __init__(self, lens):
        self.lens = lens

    def install(self):
        """
        Install patches related to this watcher
        """
        pass

    def process_request(self, request):
        """
        Process incoming request
        """
        return

    def process_response(self, request, response):
        """
        Process prepared response
        """
        return

    def uninstall(self):
        """
        Uninstall patches realted to this watcher
        """
        pass
