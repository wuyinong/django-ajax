"""
Ajax Decorators
"""
from functools import wraps
from django.http import HttpResponseBadRequest
from django.utils.decorators import available_attrs
from abalt_ajax.shortcuts import render_to_json


def ajax(function=None, mandatory=True):
    """
    Decorator who guesses the user response type and translates to a serialized
    JSON response. Usage::

        @ajax
        def my_view(request):
            do_something()
            # will send {'status': 200, 'status_text': 'OK', 'path': '/',
                         'data': null}

        @ajax
        def my_view(request):
            return {'key': 'value'}
            # will send {'status': 200, 'status_text': 'OK', 'path': '/',
                         'data': {'key': 'value'}}

        @ajax
        def my_view(request):
            return HttpResponse('<h1>Hi!</h1>')
            # will send {'status': 200, 'status_text': 'OK', 'path': '/',
                         'data': '<h1>Hi!</h1>'}

        @ajax
        def my_view(request):
            return redirect('home')
            # will send {'status': 302, 'status_text': 'FOUND', 'path': '/',
                         'location': '/'}

        # combination with others decorators:

        @ajax
        @login_required
        @require_POST
        def my_view(request):
            pass
            # if request user is not authenticated then the @login_required
            # decorator redirect to login page.
            # will send {'status': 302, 'status_text': 'FOUND', 'path': '/',
                         'location': '/login'}

            # if request method is 'GET' then the @require_POST decorator return
            # a HttpResponseNotAllowed response.
            # will send {'status': 405, 'status_text': 'METHOD NOT ALLOWED',
                         'path': '/', 'method': 'GET'}

    """
    def decorator(func):
        """
        Decorator function
        """
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            """
            Inner function
            """
            if mandatory and not request.is_ajax():
                return HttpResponseBadRequest()

            if request.is_ajax():
                try:
                    # json response
                    return render_to_json(
                        request, func(request, *args, **kwargs))
                except Exception as exception:
                    return render_to_json(request, exception)
            else:
                # conventional response
                return func(request, *args, **kwargs)

        return inner

    if function:
        return decorator(function)
    return decorator
