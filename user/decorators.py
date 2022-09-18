from django.shortcuts import redirect


def logout_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return function(request, *args, **kwargs)
    return wrapper