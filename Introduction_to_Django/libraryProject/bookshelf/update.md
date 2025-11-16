# Update the Book title

Python commands to run in the Django shell:

```py
from bookshelf.models import Book
book = Book.objects.get(pk=2)
book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(pk=2).title)
```

Expected / captured output:

```
UPDATE: Nineteen Eighty-Four
```

This shows the title was updated and saved successfully.
