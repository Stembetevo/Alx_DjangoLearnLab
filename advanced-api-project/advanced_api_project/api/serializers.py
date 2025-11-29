from rest_framework import serializers
from .models import Book, Author
from datetime import date


"""
Serializers for the `api` app.

- BookSerializer: Serializes all fields of Book and validates that
  publication_year is not in the future.

- AuthorSerializer: Serializes the author's `name` and includes a nested
  list of the author's books using `BookSerializer`. The nested serialization
  uses the `related_name='books'` declared on `Book.author`, so an author's
  books are available as `author.books.all()`.

The nested books are read-only in this serializer. To create books while
creating an author you'd implement create/update methods to handle nested
input; here we keep the nested display read-only for clarity.
"""


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model.

    - Serializes all model fields.
    - Validates that `publication_year` is not in the future.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future."""
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model including nested books.

    - `books` field uses `BookSerializer(many=True, read_only=True)` to
      serialize the related Book instances. The relation is defined by
      `Book.author` with `related_name='books'`.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        # We include `name` and the nested `books` representation
        fields = ['id', 'name', 'books']
