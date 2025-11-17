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
    template_name = 'relationship_app/registration.html'
    
