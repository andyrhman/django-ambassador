from django.core.management import BaseCommand
from faker import Faker

from core.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker('id_ID')
        
        for _ in range(30):
            user = User.objects.create(
                fullName = faker.name(),
                email = faker.email(),
                username = faker.user_name(),
                password='',
                is_ambassador=True
            )
            
            user.set_password("123123")
            user.save()