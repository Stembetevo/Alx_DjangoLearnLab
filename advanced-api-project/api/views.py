from django_filters import rest_framework
from rest_framework import viewsets, generics
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer


# -- Book generic views --
class ListView(generics.ListAPIView):
	
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	# Enable django-filter backend, search and ordering
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	# Allow filtering by these fields (including related lookups)
	filterset_fields = ['title', 'publication_year', 'author', 'author__name']
	# Enable text search on title and author name
	search_fields = ['title', 'author__name']
	# Allow ordering by these fields
	ordering_fields = ['title', 'publication_year', 'author__name']
	# Default ordering
	ordering = ['title']

class DetailView(generics.RetrieveAPIView):
	#GET /books/<pk>/  - retrieve a single book (readable by anyone)
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]




class CreateView(generics.CreateAPIView):
	#POST /books/create/ (authenticated users only).
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save()


class UpdateView(generics.UpdateAPIView):
	#PUT/PATCH /books/<pk>/update/  - update a book
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]


class DeleteView(generics.DestroyAPIView):
	#DELETE /books/<pk>/delete/  - delete a book (authenticated users only).
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]