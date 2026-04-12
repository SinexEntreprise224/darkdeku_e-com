from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # On vérifie si l'utilisateur est connecté ET s'il est admin
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)

        # Sinon, on balance un message et on redirige
        messages.error(request, "Accès interdit : cette zone est réservée à l'administrateur.")
        return redirect('index')

    return _wrapped_view