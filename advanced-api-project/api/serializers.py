"""Serializers for the `api` app.

This file contains:
- `BookSerializer`: serializes `Book` model fields and validates `publication_year`.
- `AuthorSerializer`: serializes `Author` name and includes a nested read-only
  list of serialized books for that author.

The nested relationship is implemented by adding a `books` field to
`AuthorSerializer` that uses `BookSerializer(many=True, read_only=True)` and
relies on the `related_name='books'` defined on the `Book.author` ForeignKey.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """Serializes all fields of the Book model.

    Validation:
    - `publication_year` must not be in the future.
    """

    class Meta:
        model = Book
        # include all model fields; `author` will be represented by its PK
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        if value is None:
            return value
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError('publication_year cannot be in the future')
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author and a nested, read-only list of the author's books.

    The `books` field is populated from the reverse relationship defined by
    `Book.author` (`related_name='books'`). It is read-only here because the
    requirement only asked to serialize related books dynamically.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

