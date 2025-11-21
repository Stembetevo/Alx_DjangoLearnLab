from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import ModelForm

from .models import Book


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ["title", "author", "publication_year"]


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})


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
