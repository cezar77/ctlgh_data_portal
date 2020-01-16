# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Warm up cache for CTLGH"

    main_url = 'http://data.ctlgh.org/'

    urls = {
        'sheep': 'sheep/',
        'chickens': 'chickens/',
        'ideal': 'ideal/'
    }

    def handle(self, *args, **kwargs):
        r = requests.get(self.main_url)
        sheep = requests.get(self.main_url + self.urls['sheep'])
        sheep_soup = BeautifulSoup(sheep.content, 'html.parser')
        pagination = sheep_soup.find_all('li')
        pages = pagination[len(pagination)-2]
        print(pages)
