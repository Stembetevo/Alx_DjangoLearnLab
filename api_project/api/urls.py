from django.urls import path
from .views import BookListCreateApiView


urlpatterns = [
    path('books/', BookListCreateApiView.as_view(), name='book-list'),
]