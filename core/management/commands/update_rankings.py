from django.core.management import BaseCommand
from django_redis import get_redis_connection

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        con = get_redis_connection("default")

        ambassadors = User.objects.filter(is_ambassador=True)

        for ambassador in ambassadors:
            print(ambassador.fullName, float(ambassador.revenue))
            con.zadd('rankings', {ambassador.fullName: float(ambassador.revenue)})
