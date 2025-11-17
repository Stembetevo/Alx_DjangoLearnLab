from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_member(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_MEMBER
    except Exception:
        return False


@user_passes_test(_is_member, login_url='login')
def member_view(request):
    
    context = { 'title': 'Member dashboard ' }
    return render(request, 'relationship_app/templates/relationship_app/member_view.html', context)
