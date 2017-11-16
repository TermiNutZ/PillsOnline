from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = 'Create user for tests'
    def handle(self, *args, **options):
        user = User.objects.create_user('user', 'usern@pills-online.com', 'password')