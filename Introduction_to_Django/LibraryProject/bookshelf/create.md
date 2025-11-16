# Create a Book

Python commands to run in the Django shell:

```py
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book.pk, book.title, book.author, book.publication_year)
```

Expected / captured output:

```
CREATE: 2 1984 George Orwell 1949
```

This shows the Book instance was created with primary key 2 and the requested fields.
