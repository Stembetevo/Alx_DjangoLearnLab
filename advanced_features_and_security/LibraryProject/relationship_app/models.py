from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author ,on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_add_book'),
            ('can_change_book'),
            ('can_delete_book'),
        )

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_LIBRARIAN = 'librarian'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)

    def __str__(self):
        return self.role

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True,blank=True)
    profile_photo = models.ImageField(
        upload_to='profile-photos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username