from django.contrib.auth.decorators import user_passes_test
from .models import User

def admin_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_library_admin,
        login_url="login"
    )(view_func)

def normal_user_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and not user.is_library_admin,
        login_url="login"
    )(view_func)
