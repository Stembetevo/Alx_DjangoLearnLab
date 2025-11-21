from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_librarian(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_LIBRARIAN
    except Exception:
        return False


@user_passes_test(_is_librarian, login_url='login')
def librarian_view(request):
    
    # concise title for the librarian dashboard view
    context = { 'title': 'Librarian Dashboard' }
    return render(request, 'relationship_app/templates/relationship_app/librarian_view.html', context)
