import threading
from django.utils import timezone

__author__ = 'Vishwash Gupta'
import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q
from blog.models import Keyword
from blog.utlis import scrape_from_advance_search
from blog import scrapper

class Command(BaseCommand):
    # def add_arguments(self, parser):
    #   # parser.add_argument('hello')

    def handle(self, *args, **options):
        keywords = Keyword.objects.filter(Q(last_scraped__lte=timezone.now() - datetime.timedelta(days=1)) |
                                          Q(last_scraped__isnull=True))
        for keyword in keywords:
            try:
                scrape_from_advance_search(keyword)
                # t = threading.Thread(target=scrape_from_advance_search, args=(keyword,))
                # t.start()

            except Exception, e:
                print "error in scraping for keyword %s", keyword.name
                print e