from functools import wraps
from django.http import HttpResponseForbidden

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this endpoint.")
        return _wrapped_view
    return decorator
