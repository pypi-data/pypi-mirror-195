from pathlib import Path
from django import template
from django.utils.safestring import SafeText

register = template.Library()

@register.filter
def colorize_method(method):
    if method == "GET":
        return "bg-blue-500"
    elif method in ["POST", "PUT", "PATCH"]:
        return "bg-green-500"
    elif method == "DELETE":
        return "bg-red-500"
    else:
        return "bg-yellow-500"


@register.filter
def colorize_status(status):
    if status >= 100 and status < 300:
        return "bg-green-500"
    elif status >= 300 and status < 400:
        return "bg-blue-500"
    elif status >= 400 and status < 500:
        return "bg-yellow-500"
    else:
        return "bg-red-500"

@register.filter
def highlight_filename(filename):
    path =  Path(filename)
    return SafeText(f"{path.parent}/<strong>{path.name}</strong>")
