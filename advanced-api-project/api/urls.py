from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AuthorViewSet,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    # Book generic view endpoints
    path('books/', ListView.as_view(), name='book-list'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/update', UpdateView.as_view(), name='book-update'),
    path('books/delete', DeleteView.as_view(), name='book-delete'),

    # Author viewset endpoints (router)
    path('', include(router.urls)),
]
