from django.core.management.base import BaseCommand
from advocoders import utils


class Command(BaseCommand):

    help = 'Updates all RSS feeds'

    def handle(self, *args, **options):
        utils.update_feeds()
