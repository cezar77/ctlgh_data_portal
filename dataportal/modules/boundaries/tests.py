import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from dataportal.modules.boundaries.models import Country


class CountryViewSetTestCase(TestCase):
    fixtures = ['country.json']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        cls.countries = Country.objects.all()
        cls.eth = Country.objects.get(iso='ETH')
        cls.lby = Country.objects.get(iso='LBY')
        cls.user = User.objects.create_user(
            'Test',
            'test@example.com',
            'testpass'
        ) 

    def test_create_country(self):
        """
        Test create
        """
        url = reverse('boundaries:country-list')
        with open('dataportal/modules/boundaries/fixtures/nigeria.json') as f:
            data = json.load(f)
        self.client.force_login(self.user)
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        country = Country.objects.get(iso='NGA')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['iso'], country.iso)

    def test_list_countries(self):
        """
        Test list
        """
        url = reverse('boundaries:country-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.countries.count())
        self.assertEqual(response.data[0]['iso'], self.eth.iso)
        self.assertEqual(response.data[1]['iso'], self.lby.iso)

    def test_retrieve_country(self):
        """
        Test retrieve
        """
        url = reverse(
            'boundaries:country-detail',
            kwargs={'iso': self.eth.iso}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name_english'], self.eth.name_english)

    def test_update_country(self):
        """
        Test update
        """
        url = reverse(
            'boundaries:country-detail',
            kwargs={'iso': self.eth.iso}
        )
        with open('dataportal/modules/boundaries/fixtures/ethiopia_update.json') as  f:
            data = json.load(f)
        self.client.force_login(self.user)
        response = self.client.put(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        eth = Country.objects.get(iso='ETH')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['pop2000'], eth.pop2000)
        self.assertEqual(response.data['sqkm'], eth.sqkm)
        self.assertEqual(response.data['popsqkm'], eth.popsqkm)

    def test_delete_country(self):
        """
        Test delete
        """
        url = reverse(
            'boundaries:country-detail',
            kwargs={'iso': self.eth.iso}
        )
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
