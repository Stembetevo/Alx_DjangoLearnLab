from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import ModelForm, Form, CharField
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Book
from .forms import ExampleForm


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ["title", "author", "publication_year"]


class SearchForm(Form):
	q = CharField(max_length=100, required=False)

	def clean_q(self):
		value = self.cleaned_data.get('q', '')
		value = value.strip()
		# Basic validation: limit length and forbid suspicious input
		if len(value) > 100:
			raise ValidationError('Search query too long')
		return value


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
	# Provide optional search via GET ?q=...
	form = SearchForm(request.GET)
	if form.is_valid():
		q = form.cleaned_data.get('q')
		if q:
			# Use ORM parameterized lookups to avoid SQL injection
			books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
		else:
			books = Book.objects.all()
	else:
		# On invalid input, default to empty queryset to be safe
		books = Book.objects.none()
	return render(request, 'bookshelf/book_list.html', {'books': books, 'search_form': form})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, pk):
	book = get_object_or_404(Book, pk=pk)
	return render(request, 'bookshelf/book_detail.html', {'book': book})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			# Using ModelForm ensures data is validated/cleaned before saving
			form.save()
			return redirect('bookshelf:list_books')
	else:
		form = BookForm()
	return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			return redirect('bookshelf:view_book', pk=book.pk)
	else:
		form = BookForm(instance=book)
	return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		book.delete()
		return redirect('bookshelf:list_books')
	return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
def example_form(request):
	"""Render a simple example form. If the user has `bookshelf.can_create`, allow
	creating a `Book` from the submitted data; otherwise add a non-field error.
	This demonstrates secure form handling and permission checks.
	"""
	if request.method == 'POST':
		form = ExampleForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if request.user.has_perm('bookshelf.can_create'):
				Book.objects.create(
					title=data.get('title'),
					author=data.get('author'),
					publication_year=data.get('publication_year') or None,
				)
				return redirect('bookshelf:list_books')
			else:
				form.add_error(None, 'You do not have permission to create a book.')
	else:
		form = ExampleForm()
	return render(request, 'bookshelf/form_example.html', {'form': form})
