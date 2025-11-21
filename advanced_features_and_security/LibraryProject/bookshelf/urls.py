from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('book/<int:pk>/', views.view_book, name='view_book'),
    path('book/create/', views.create_book, name='create_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('example-form/', views.example_form, name='example_form'),
]
