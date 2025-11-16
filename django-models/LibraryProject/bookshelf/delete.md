# Delete the Book

Python commands to run in the Django shell:

```py
from bookshelf.models import Book
book = Book.objects.get(pk=2)
book.delete()
print(Book.objects.count())
```

Expected / captured output:

```
COUNT AFTER DELETE: 0
```

This confirms the Book instance was deleted and there are no Book records left.
