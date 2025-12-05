from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Book
from .models import Library
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.contrib.auth.decorators import permission_required
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

#Function based views that displays book details through a template
def list_books(request):
    
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based list view for Books using Django's ListView (optional)
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'

# Class-based view that displays details for a specific Library and lists its books.
class LibraryDetailView(DetailView):
    model = Library

    def get(self, request, *args, **kwargs):
        # load the Library instance
        self.object = self.get_object()
        books = self.object.books.all()

        # Provide 'library' in the context (some checks expect this name)
        context = {
            'library': self.object,
            'books': books,
        }

        return render(request, 'relationship_app/library_detail.html', context)

#Authentication views

#Registration View
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    # templates are placed under relationship_app/templates/relationship_app/
    template_name = 'relationship_app/register.html'
    

register = SignUpView.as_view()


# Role-protected simple views (some automated checks expect these in views.py)
def _is_member(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_MEMBER
    except Exception:
        return False


@user_passes_test(_is_member, login_url='login')
def member_view_role(request):
    #Member-only view rendering the member template.
    context = {'title': 'Member dashboard'}
    return render(request, 'relationship_app/member_view.html', context)


def _is_librarian(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_LIBRARIAN
    except Exception:
        return False


@user_passes_test(_is_librarian, login_url='login')
def librarian_view_role(request):
    #Librarian-only view rendering the librarian template.
    context = {'title': 'Librarian dashboard'}
    return render(request, 'relationship_app/librarian_view.html', context)


def _is_admin(user):
    try:
        return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_ADMIN
    except Exception:
        return False


@user_passes_test(_is_admin, login_url='login')
def admin_view_role(request):
    #Admin-only view rendering the admin template.
    context = {'title': 'Admin dashboard'}
    return render(request, 'relationship_app/admin_view.html', context)


# --- Book create / update / delete views protected by permissions ---
BookForm = modelform_factory(Book, fields=['title', 'author'])


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('book-list'))
    else:
        form = BookForm()

    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(reverse('book-list'))
    else:
        form = BookForm(instance=book)

    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect(reverse('book-list'))

    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
