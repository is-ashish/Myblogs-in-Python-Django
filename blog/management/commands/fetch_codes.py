from blog.utlis import scrape_codes

__author__ = 'Vishwash Gupta'
from django.core.management.base import BaseCommand
import threading
from BeautifulSoup import BeautifulSoup
from django.utils import timezone
import requests



class Command(BaseCommand):
    # def add_arguments(self, parser):
    #   # parser.add_argument('hello')

    def handle(self, *args, **options):
        scrape_codes()


