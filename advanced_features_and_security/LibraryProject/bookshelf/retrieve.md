# Retrieve the Book

Python commands to run in the Django shell:

```py
from bookshelf.models import Book
book = Book.objects.get(pk=2)
print(book.pk, book.title, book.author, book.publication_year)
```

Expected / captured output:

```
RETRIEVE: 2 1984 George Orwell 1949
```

This shows the Book instance with primary key 2 and all fields.
