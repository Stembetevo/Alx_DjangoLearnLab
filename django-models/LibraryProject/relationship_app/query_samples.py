import os
import sys
from typing import Iterable, Optional


def django_setup():
    here = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(here, os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libraryProject.settings")
    import django

    django.setup()


def get_books_by_author(author_name: str):
    """Return all Book objects written by the given author's name."""
    from relationship_app.models import Book

    # filter by related field value
    return Book.objects.filter(author__name=author_name)


def list_books_in_library(library_name: str):
    """Return all Book objects that are related to the named Library."""
    from relationship_app.models import Library

    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Library.objects.none()

    return lib.books.all()


def get_librarian_for_library(library_name: str):
    """Return the Librarian instance for the given library name, or None if not found."""
    from relationship_app.models import Library, Librarian

    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    # OneToOneField creates a reverse attribute on Library with the lowercase model name by default
    try:
        return lib.librarian
    except Librarian.DoesNotExist:
        return None


def _demo():
    author_name = "George Orwell"
    library_name = "Central Library"

    print(f"Books by author: {author_name}")
    for b in get_books_by_author(author_name):
        print(f"- {b.title} (id={b.pk})")

    print(f"\nBooks in library: {library_name}")
    for b in list_books_in_library(library_name):
        print(f"- {b.title} by {b.author.name}")

    print(f"\nLibrarian for library: {library_name}")
    libn = get_librarian_for_library(library_name)
    if libn:
        print(f"- {libn.name} (id={libn.pk})")
    else:
        print("- No librarian found for that library.")


if __name__ == "__main__":
    django_setup()
    _demo()
