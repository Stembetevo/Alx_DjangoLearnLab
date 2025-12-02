from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book
import json


class SimpleBookAPITests(APITestCase):
	def setUp(self):
		# create a user for authenticated operations
		self.user = User.objects.create_user(username='tester', password='pass')

		# create an author and two books
		self.author = Author.objects.create(name='Author One')
		self.book1 = Book.objects.create(title='Alpha', publication_year=2000, author=self.author)
		self.book2 = Book.objects.create(title='Beta', publication_year=2010, author=self.author)

		# named URLs from api/urls.py (project includes these under 'api/')
		self.list_url = reverse('book-list')
		self.create_url = reverse('book-create')
		self.detail_url = lambda pk: reverse('book-detail', args=[pk])
		self.update_url = lambda pk: reverse('book-update', args=[pk])
		self.delete_url = lambda pk: reverse('book-delete', args=[pk])

	def test_list_books(self):
		resp = self.client.get(self.list_url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		# parse JSON response body
		data = json.loads(resp.content)
		# Expect two books
		self.assertEqual(len(data), 2)

	def test_filter_by_title(self):
		resp = self.client.get(self.list_url, {'title': 'Alpha'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		data = json.loads(resp.content)
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]['title'], 'Alpha')

	def test_search_and_ordering(self):
		# search should match 'Alpha' and ordering should sort by publication_year desc
		resp = self.client.get(self.list_url, {'search': 'Alph', 'ordering': '-publication_year'})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		# ensure Alpha is present
		titles = [b['title'] for b in data]
		self.assertIn('Alpha', titles)

	def test_retrieve_book(self):
		resp = self.client.get(self.detail_url(self.book1.pk))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json().get('title'), 'Alpha')

	def test_create_requires_auth_and_creates(self):
		payload = {'title': 'Gamma', 'publication_year': 2021, 'author': self.author}
		# unauthenticated should not create
		resp = self.client.post(self.create_url, data=json.dumps(payload), content_type='application/json')
		self.assertNotEqual(resp.status_code, 201)

		# authenticate and create
		self.client.force_login(self.user)
		resp = self.client.post(self.create_url, data=json.dumps(payload), content_type='application/json')
		self.assertEqual(resp.status_code, 201)
		self.assertTrue(Book.objects.filter(title='Gamma').exists())

	def test_update_requires_auth_and_updates(self):
		update_payload = {'title': 'Alpha Updated', 'publication_year': 2001, 'author': self.author}
		# unauthenticated update should fail
		resp = self.client.put(self.update_url(self.book1.pk), data=json.dumps(update_payload), content_type='application/json')
		self.assertNotEqual(resp.status_code, 200)

		# authenticate and update
		self.client.force_login(self.user)
		resp = self.client.put(self.update_url(self.book1.pk), data=json.dumps(update_payload), content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		self.book1.refresh_from_db()
		self.assertEqual(self.book1.title, 'Alpha Updated')

	def test_delete_requires_auth_and_deletes(self):
		# unauthenticated delete should fail
		resp = self.client.delete(self.delete_url(self.book2.pk))
		self.assertNotEqual(resp.status_code, 204)

		# authenticate and delete
		self.client.force_login(self.user)
		resp = self.client.delete(self.delete_url(self.book2.pk))
		# DRF may return 204 No Content or 200 OK depending on configuration
		self.assertIn(resp.status_code, (200, 204))
		self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

# Create your tests here.
