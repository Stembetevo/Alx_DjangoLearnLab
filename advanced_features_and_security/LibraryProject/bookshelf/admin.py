from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "publication_year")
	list_filter = ("publication_year", "author")
	search_fields = ("title", "author")

class CustomUserAdmin(UserAdmin):
	model = CustomUser
	fieldsets = UserAdmin.fieldsets + (
		('Additional', { 'fields': ('date_of_birth', 'profile_photo')}),
	)

	add_fieldsets = UserAdmin.add_fieldsets + (
		('Additional', { 'classes': ('wide',), 'fields': ('date_of_birth', 'profile_photo')}),
	)

	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

	search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(CustomUser,CustomUserAdmin)