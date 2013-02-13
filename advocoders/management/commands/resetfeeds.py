from django.core.management.base import BaseCommand
from advocoders import utils
from advocoders.models import Content


class Command(BaseCommand):

    help = 'Deletes all content, and updates all RSS feeds'

    def handle(self, *args, **options):
        Content.objects.all().delete()
        utils.update_feeds()
