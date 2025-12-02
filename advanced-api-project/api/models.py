from django.db import models


class Author(models.Model):
	"""Represents a book author.

	Fields:
	- name: author full name (string)

	The relationship to `Book` is one-to-many: an Author may have many Books.
	The reverse relation is available via the `books` related name on Book.
	"""

	name = models.CharField(max_length=120)

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.name


class Book(models.Model):
	"""Represents a book written by an Author.

	Fields:
	- title: the book title (string)
	- publication_year: integer year when the book was published
	- author: ForeignKey to `Author` establishing a one-to-many relationship
	"""

	title = models.CharField(max_length=255)
	publication_year = models.PositiveIntegerField(null=True, blank=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.title
