"""
Taken from django-debug-toolbar

Copyright (c) Rob Hudson and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re

import sqlparse
from sqlparse import tokens as T
from django.utils.html import escape

from functools import lru_cache

import linecache
import sys
import inspect

from django.template import Node
from asgiref.local import Local

_local_data = Local()

def getframeinfo(frame, context=1):
    """
    Get information about a frame or traceback object.
    A tuple of five things is returned: the filename, the line number of
    the current line, the function name, a list of lines of context from
    the source code, and the index of the current line within that list.
    The optional second argument specifies the number of lines of context
    to return, which are centered around the current line.
    This originally comes from ``inspect`` but is modified to handle issues
    with ``findsource()``.
    """
    if inspect.istraceback(frame):
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
    if not inspect.isframe(frame):
        raise TypeError("arg is not a frame or traceback object")

    filename = inspect.getsourcefile(frame) or inspect.getfile(frame)
    if context > 0:
        start = lineno - 1 - context // 2
        try:
            lines, lnum = inspect.findsource(frame)
        except Exception:  # findsource raises platform-dependant exceptions
            lines = index = None
        else:
            start = max(start, 1)
            start = max(0, min(start, len(lines) - context))
            lines = lines[start : (start + context)]
            index = lineno - 1 - start
    else:
        lines = index = None

    return inspect.Traceback(filename, lineno, frame.f_code.co_name, lines, index)


def get_stack(context=1):
    """
    Get a list of records for a frame and all higher (calling) frames.
    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context.
    Modified version of ``inspect.stack()`` which calls our own ``getframeinfo()``
    """
    frame = sys._getframe(1)
    framelist = []
    while frame:
        framelist.append((frame,) + getframeinfo(frame, context))
        frame = frame.f_back
    return framelist


def _stack_frames(*, skip=0):
    skip += 1  # Skip the frame for this generator.
    frame = inspect.currentframe()
    while frame is not None:
        if skip > 0:
            skip -= 1
        else:
            yield frame
        frame = frame.f_back


def _is_excluded_frame(frame, excluded_modules) -> bool:
    if not excluded_modules:
        return False
    frame_module = frame.f_globals.get("__name__")
    if not isinstance(frame_module, str):
        return False
    return any(
        frame_module == excluded_module
        or frame_module.startswith(excluded_module + ".")
        for excluded_module in excluded_modules
    )


def get_stack_trace(*, skip=0):
    """
    Return a processed stack trace for the current call stack.
    If the ``ENABLE_STACKTRACES`` setting is False, return an empty :class:`list`.
    Otherwise return a :class:`list` of processed stack frame tuples (file name, line
    number, function name, source line, frame locals) for the current call stack.  The
    first entry in the list will be for the bottom of the stack and the last entry will
    be for the top of the stack.
    ``skip`` is an :class:`int` indicating the number of stack frames above the frame
    for this function to omit from the stack trace.  The default value of ``0`` means
    that the entry for the caller of this function will be the last entry in the
    returned stack trace.
    """
    skip += 1  # Skip the frame for this function.
    stack_trace_recorder = getattr(_local_data, "stack_trace_recorder", None)
    if stack_trace_recorder is None:
        stack_trace_recorder = _StackTraceRecorder()
        _local_data.stack_trace_recorder = stack_trace_recorder
    return stack_trace_recorder.get_stack_trace(
        excluded_modules=[
            "socketserver",
            "threading",
            "wsgiref",
            "debug_toolbar",
            "lens",
            "django.db",
            "django.core.handlers",
            "django.core.servers",
            "django.utils.decorators",
            "django.utils.deprecation",
            "django.utils.functional",
        ],
        include_locals=False,
        skip=skip,
    )


class _StackTraceRecorder:
    def __init__(self):
        self.filename_cache = {}

    def get_source_file(self, frame):
        frame_filename = frame.f_code.co_filename

        value = self.filename_cache.get(frame_filename)
        if value is None:
            filename = inspect.getsourcefile(frame)
            if filename is None:
                is_source = False
                filename = frame_filename
            else:
                is_source = True
                # Ensure linecache validity the first time this recorder
                # encounters the filename in this frame.
                linecache.checkcache(filename)
            value = (filename, is_source)
            self.filename_cache[frame_filename] = value

        return value

    def get_stack_trace(
        self,
        *,
        excluded_modules = None,
        include_locals: bool = False,
        skip: int = 0,
    ):
        trace = []
        skip += 1  # Skip the frame for this method.
        for frame in _stack_frames(skip=skip):
            if _is_excluded_frame(frame, excluded_modules):
                continue

            filename, is_source = self.get_source_file(frame)

            line_no = frame.f_lineno
            func_name = frame.f_code.co_name

            if is_source:
                module = inspect.getmodule(frame, filename)
                module_globals = module.__dict__ if module is not None else None
                source_line = linecache.getline(
                    filename, line_no, module_globals
                ).strip()
            else:
                source_line = ""

            frame_locals = frame.f_locals if include_locals else None

            trace.append((filename, line_no, func_name, source_line, frame_locals))
        trace.reverse()
        return trace


def get_template_info():
    template_info = None
    cur_frame = sys._getframe().f_back
    try:
        while cur_frame is not None:
            in_utils_module = cur_frame.f_code.co_filename.endswith(
                "/debug_toolbar/utils.py"
            )
            is_get_template_context = (
                cur_frame.f_code.co_name == get_template_context.__name__
            )
            if in_utils_module and is_get_template_context:
                # If the method in the stack trace is this one
                # then break from the loop as it's being check recursively.
                break
            elif cur_frame.f_code.co_name == "render":
                node = cur_frame.f_locals["self"]
                if isinstance(node, Node):
                    context = cur_frame.f_locals["context"]
                    template_info = get_template_context(node, context)
                    break
            cur_frame = cur_frame.f_back
    except Exception as e:
        pass
    del cur_frame
    return template_info



def get_template_context(node, context, context_lines=3):
    line, source_lines, name = get_template_source_from_exception_info(node, context)
    debug_context = []
    start = max(1, line - context_lines)
    end = line + 1 + context_lines

    for line_num, content in source_lines:
        if start <= line_num <= end:
            debug_context.append(
                {"num": line_num, "content": content, "highlight": (line_num == line)}
            )

    return {"name": name, "context": debug_context}


def get_template_source_from_exception_info(node, context):
    if context.template.origin == node.origin:
        exception_info = context.template.get_exception_info(
            Exception("DDT"), node.token
        )
    else:
        exception_info = context.render_context.template.get_exception_info(
            Exception("DDT"), node.token
        )
    line = exception_info["line"]
    source_lines = exception_info["source_lines"]
    name = exception_info["name"]
    return line, source_lines, name

"""
More copied code from django-debug-toolbar/sql
"""

def reformat_sql(sql):
    formatted = parse_sql(sql, aligned_indent=True)
    simple = simplify(parse_sql(sql, aligned_indent=False))
    return {
        "raw_sql": sql,
        "formatted_sql": formatted,
        "simple_sql": simple
    }


def parse_sql(sql, aligned_indent=False):
    return _parse_sql(sql, True, aligned_indent)


@lru_cache(maxsize=128)
def _parse_sql(sql, pretty, aligned_indent):
    stack = get_filter_stack(pretty, aligned_indent)
    return "".join(stack.run(sql))


@lru_cache(maxsize=None)
def get_filter_stack(prettify, aligned_indent):
    stack = sqlparse.engine.FilterStack()
    if prettify:
        stack.enable_grouping()
    if aligned_indent:
        stack.stmtprocess.append(
            sqlparse.filters.AlignedIndentFilter()
        )
    stack.postprocess.append(sqlparse.filters.SerializerUnicode())  # tokens -> strings
    return stack


simplify_re = re.compile(r"SELECT (...........*?) FROM")


def simplify(sql):
    return simplify_re.sub(r"SELECT ... FROM", sql)

