from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Movie

class TestMovieViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie1 = Movie.objects.create(name='Test Movie 1', year=2020, genre='Action', imdb_rating=8.0)

    def test_list_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'search': 'Test Movie 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_movies_by_imdb_rating(self):
        url = reverse('movie-list')
        response_asc = self.client.get(url, {'ordering': 'imdb_rating'})
        response_desc = self.client.get(url, {'ordering': '-imdb_rating'})
        self.assertEqual(response_asc.status_code, status.HTTP_200_OK)
        self.assertEqual(response_desc.status_code, status.HTTP_200_OK)
        self.assertEqual(response_asc.data[0]['name'], 'Test Movie 1')
