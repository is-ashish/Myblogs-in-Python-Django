__author__ = 'Vishwash Gupta'
import threading
from django.utils import timezone
import datetime
from django.core.management.base import BaseCommand
from blog.models import UserRequest
from blog.utils import scrape_user_request_opportunities_in_selenium


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #   # parser.add_argument('hello')

    def handle(self, *args, **options):
        user_requests = UserRequest.objects.all()
        for user_request in user_requests:
            if user_request.last_scraped is None or user_request.last_scraped <= timezone.now() - datetime.timedelta(days=1):
                    scrape_user_request_opportunities_in_selenium(user_request)