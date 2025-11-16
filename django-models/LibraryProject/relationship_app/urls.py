from django.urls import path
from . import views

urlpatterns = [
    # List all books (function-based view)
    path('books/', views.list_books, name='book-list'),

    # Class-based list view for books (alternative)
    path('books-class/', views.BookListView.as_view(), name='book-list-class'),

    # Library detail (class-based DetailView) - expects a PK parameter
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]