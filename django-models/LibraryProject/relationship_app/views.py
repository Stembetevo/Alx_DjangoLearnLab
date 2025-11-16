from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Library


def list_books(request):
    
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view that displays details for a specific Library and lists its books.
class LibraryDetailView(DetailView):
    model = Library

    def get(self, request, *args, **kwargs):
        # load the Library instance
        self.object = self.get_object()
        books = self.object.books.all()

        lines = [f"Library: {self.object.name}"]
        for book in books:
            title = getattr(book, 'title', None) or str(book)
            # book.author on this project is a FK to Author in relationship_app.models
            author = getattr(book, 'author', None)
            # If author is an object, try to use its name attribute
            if getattr(author, 'name', None):
                author_name = author.name
            else:
                author_name = str(author) if author is not None else 'Unknown'
            lines.append(f"{title} — {author_name}")

        if len(lines) == 1:
            body = f"No books found in {self.object.name}."
        else:
            body = "\n".join(lines)

        return HttpResponse(body, content_type="text/plain")
    

    


