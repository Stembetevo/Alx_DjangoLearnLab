from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
