from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from environ import Env

env = Env()
User = get_user_model()


class Command(BaseCommand):
    help = 'Generate Superuser, If none exist!'

    def handle(self, *args, **options):
        admin_exist = User.objects.filter(
            is_superuser=True
        ).count()

        if admin_exist == 0:
            admin_user = User.objects.create_superuser(
                username=env("DJANGO_SUPERUSER_USERNAME"),
                email=env("DJANGO_SUPERUSER_EMAIL"),
                password=env("DJANGO_SUPERUSER_PASSWORD"),
                phone_number=env("DJANGO_SUPERUSER_PHONE")
            )
            admin_user.save()

            self.stdout.write(self.style.SUCCESS('Successfully added Superuser'))
        else:
            pass
