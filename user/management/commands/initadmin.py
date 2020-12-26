from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from environ import Env

env = Env()
User = get_user_model()


class Command(BaseCommand):
    help = 'Generate Superuser, If none exist!'

    def handle(self, *args, **options):
        admin_exist = User.objects.filter(is_superuser=True).count()
        
        if admin_exist == 0:
            admin_user = User.objects.create_superuser(
                username=env("DJANGO_SU_NAME"),
                email=env("DJANGO_SU_EMAIL"),
                password=env("DJANGO_SU_PASS"),
                phone_number=env("DJANGO_SU_PHONE")
            )
            admin_user.save()

            self.stdout.write(self.style.SUCCESS('Successfully added Superuser'))
        else:
            pass
