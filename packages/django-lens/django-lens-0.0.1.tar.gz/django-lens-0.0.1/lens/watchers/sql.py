import logging
import time
from contextlib import contextmanager

from django.db import connections
from django.db.backends.utils import CursorWrapper
from django.utils import timezone

from lens import traces

from ..models import Trace
from ..utils import get_stack_trace, reformat_sql
from .base import Watcher

django_db_logger = logging.getLogger("django.db.backends")


class LensCursorWrapper(CursorWrapper):
    """
    Wrapper for logging SQL query traces. Based on Django's CursorDebugWrapper.
    """

    def __init__(self, lens, cursor, db):
        self.lens = lens
        super().__init__(cursor, db)

    def execute(self, sql, params=None):
        with self.debug_sql(sql, params, use_last_executed_query=True):
            return super().execute(sql, params)

    def executemany(self, sql, param_list):
        with self.debug_sql(sql, param_list, many=True):
            return super().executemany(sql, param_list)

    @contextmanager
    def debug_sql(
        self, sql=None, params=None, use_last_executed_query=False, many=False
    ):
        start = time.monotonic()
        start_time = timezone.now()
        try:
            yield
        finally:
            stop = time.monotonic()
            stop_time = timezone.now()
            duration = stop - start
            if use_last_executed_query:
                sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            try:
                times = len(params) if many else ""
            except TypeError:
                # params could be an iterator.
                times = "?"

            # Django's query logger implementation
            self.db.queries_log.append(
                {
                    "sql": "%s times: %s" % (times, sql) if many else sql,
                    "time": "%.3f" % duration,
                }
            )
            django_db_logger.debug(
                "(%.3f) %s; args=%s",
                duration,
                sql,
                params,
                extra={"duration": duration, "sql": sql, "params": params},
            )

            trace = {
                **reformat_sql("%s times: %s" % (times, sql) if many else sql),
                "duration": "%.3f" % duration,
                "start_time": start_time,
                "end_time": stop_time,
                "alias": self.db.alias,
                "stacktrace": get_stack_trace(skip=2),
            }
            traces.add(
                Trace(
                    type="sql",
                    request_id=self.lens.request_id,
                    start_time=trace["start_time"],
                    end_time=trace["end_time"],
                    data=trace,
                )
            )


class SQLWatcher(Watcher):
    def install(self):
        for connection in connections.all():
            if hasattr(connection, "_original_cursor"):
                continue

            connection._original_cursor = connection.cursor

            def cursor(*args, **kwargs):
                return LensCursorWrapper(
                    self.lens, connection._original_cursor(*args, **kwargs), connection
                )

            connection.cursor = cursor

    def uninstall(self):
        for connection in connections.all():
            if hasattr(connection, "_original_cursor"):
                connection.cursor = connection._original_cursor
                del connection._original_cursor
