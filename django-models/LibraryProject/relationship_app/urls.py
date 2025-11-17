from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from . import views


urlpatterns = [
    # List all books (function-based view)
    path('books/', list_books, name='book-list'),

    # Class-based list view for books (alternative)
    path('books-class/', views.BookListView.as_view(), name='book-list-class'),

    # Library detail (class-based DetailView) - expects a PK parameter
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),

    # Class based authentication views
    # expose a function-like reference to the registration view (views.register will be created)
    path('registration/', views.register, name="registration"),

    # template paths include the app folder (relationship_app)
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name="login"),

    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout")
]