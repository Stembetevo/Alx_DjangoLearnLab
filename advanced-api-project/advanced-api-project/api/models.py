from django.db import models


"""
Data models for the `api` app.

Models:
 - Author: Represents a book author. Contains the author's name.
 - Book: Represents a published book. Contains title, publication year,
   and a foreign key to the Author that wrote the book.

The `Author` -> `Book` relationship is one-to-many: one Author can have
multiple Book instances. The `Book.author` field uses `related_name='books'`
so that an author's books can be accessed with `author.books.all()`.
"""


class Author(models.Model):
	"""An author of one or more books.

	Fields
	- name: The full name of the author.
	"""

	name = models.CharField(max_length=255)

	def __str__(self) -> str:  # human-readable representation
		return self.name


class Book(models.Model):
	"""A book written by an Author.

	Fields
	- title: The book's title.
	- publication_year: Integer year the book was published.
	- author: ForeignKey to `Author`, establishing many books -> one author.
	"""

	title = models.CharField(max_length=255)
	publication_year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self) -> str:
		return f"{self.title} ({self.publication_year})"

