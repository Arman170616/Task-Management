from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You are not authorized to access this resource.")
        return wrapper
    return decorator
