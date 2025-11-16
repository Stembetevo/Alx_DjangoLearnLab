# CRUD operations performed in the Django shell

Below are the commands used and the captured outputs when running a short Django-aware script that performed the create, retrieve, update and delete sequence.

Commands and outputs (combined):

```py
from bookshelf.models import Book
# Cleanup any pre-existing test entries
Book.objects.filter(title="1984").delete()

# Create
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print("CREATE:", book.pk, book.title, book.author, book.publication_year)

# Retrieve
book = Book.objects.get(pk=book.pk)
print("RETRIEVE:", book.pk, book.title, book.author, book.publication_year)

# Update
book.title = "Nineteen Eighty-Four"
book.save()
print("UPDATE:", Book.objects.get(pk=book.pk).title)

# Delete
book.delete()
print("COUNT AFTER DELETE:", Book.objects.count())
```

Captured output from the run:

```
CREATE: 2 1984 George Orwell 1949
RETRIEVE: 2 1984 George Orwell 1949
UPDATE: Nineteen Eighty-Four
COUNT AFTER DELETE: 0
```

Notes:
- The exact primary key (here `2`) may differ on another system or if other records exist; the important part is that the object was created, retrieved, updated and deleted successfully.
- If you prefer to run these interactively, open the Django shell with:

```bash
python3 manage.py shell
```

and run the Python commands shown above.
