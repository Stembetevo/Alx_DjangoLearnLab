from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer


# -- Book generic views --
class ListView(generics.ListAPIView):
	#GET /books/  - list all books 
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


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