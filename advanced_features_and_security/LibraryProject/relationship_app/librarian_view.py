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
    
    context = { 'title': 'LibrarianFor each role, create an HTML template to display relevant content when users access their respective views.

Templates to Create:

admin_view.html for Admin users.
librarian_view.html for Librarians.
member_view.html for Members. dashboard ' }
    return render(request, 'relationship_app/templates/relationship_app/librarian_view.html', context)
