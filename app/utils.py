import inspect

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def add_function_body_as_kwarg(func):
    function_body = inspect.getsource(func)
    function_body = function_body.replace('@add_function_body_as_kwarg\n', '')
    function_body = highlight(function_body,
                              PythonLexer(),
                              HtmlFormatter(linenos=True, noclasses=True))

    def f(*args, **kwargs):
        return func(*args, function_body=function_body, **kwargs)

    return f
