Bookshelf app — Permissions & Groups

This document explains the custom permissions added to the `Book` model, how to create groups, assign permissions, and how the views enforce them.

1) Custom permissions
- Defined on `bookshelf.models.Book` (see `Meta.permissions`):
  - `can_view`  — Allows listing and viewing book details
  - `can_create` — Allows creating new books
  - `can_edit`  — Allows editing existing books
  - `can_delete` — Allows deleting books

These permissions are registered when you run migrations (`python manage.py makemigrations` and `python manage.py migrate`).

2) Groups to create (examples)
- `Viewers`: assign `can_view`
- `Editors`: assign `can_view`, `can_create`, `can_edit`
- `Admins`: assign all permissions (plus staff/superuser flags as needed)

3) How to create groups and assign permissions (Admin site)
- Login to Django admin (`/admin/`) as a superuser.
- Go to "Groups" → "Add Group".
- Create a group like `Editors` and in "Permissions" pick the `Book` permissions (`Can view book`, `Can create book`, ...).
- Save.
- Assign users to groups via the user's admin page.

4) Programmatic setup (manage.py shell)

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

ct = ContentType.objects.get_for_model(Book)

# Create groups
viewers, _ = Group.objects.get_or_create(name='Viewers')
editors, _ = Group.objects.get_or_create(name='Editors')
admins, _ = Group.objects.get_or_create(name='Admins')

# Get permissions by codename (codenames defined on the model Meta)
can_view = Permission.objects.get(content_type=ct, codename='can_view')
can_create = Permission.objects.get(content_type=ct, codename='can_create')
can_edit = Permission.objects.get(content_type=ct, codename='can_edit')
can_delete = Permission.objects.get(content_type=ct, codename='can_delete')

# Assign permissions to groups
viewers.permissions.set([can_view])
editors.permissions.set([can_view, can_create, can_edit])
admins.permissions.set([can_view, can_create, can_edit, can_delete])

# Save (get_or_create already saved, but safe to ensure)
viewers.save()
editors.save()
admins.save()
```

5) Views enforcement
- Views in `bookshelf/views.py` use the decorator `@permission_required('bookshelf.can_edit', raise_exception=True)` etc.
- If a user does not have the required permission, a `PermissionDenied` exception is raised (HTTP 403) or they can be redirected depending on your global auth setup.

6) Templates / URLs
- The views render templates named:
  - `bookshelf/book_list.html`
  - `bookshelf/book_detail.html`
  - `bookshelf/book_form.html`
  - `bookshelf/book_confirm_delete.html`

- Add URL routes for these views in a `bookshelf/urls.py` (not provided) and include them in the project `urls.py`.

7) Testing manually
- Create a normal user and assign them to a group (e.g., `Viewers`) and verify they can list and view books but not create/edit/delete.
- Create a user in `Editors` and verify create/edit works, but delete does not.
- Use the Django admin or the shell to confirm permission assignments.

Notes
- The permission codenames are intentionally short (`can_view`, `can_create`, `can_edit`, `can_delete`) to match the task requirement. When referencing them in `@permission_required`, include the app label: `bookshelf.can_edit`.
- Remember to run migrations after changing `models.py`:

```
python manage.py makemigrations bookshelf
python manage.py migrate
```

