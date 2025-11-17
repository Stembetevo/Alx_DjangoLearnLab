from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_admin(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_ADMIN
    except Exception:
        return False


@user_passes_test(_is_admin, login_url='login')
def admin_view(request):
    
    context = { 'title': 'Admin dashboard ' }
    return render(request, 'relationship_app/templates/relationship_app/admin_view.html', context)
