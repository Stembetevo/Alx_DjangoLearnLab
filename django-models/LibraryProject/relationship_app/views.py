from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Library

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
    

    


