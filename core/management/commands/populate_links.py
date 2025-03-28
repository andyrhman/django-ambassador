from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Link, Product, User

class Command(BaseCommand):
    help = "Seed orders and order items data"

    def handle(self, *args, **kwargs):
        faker = Faker("id_ID")
        users = User.objects.all()
        products = Product.objects.all() #pyright: ignore

        for i in range(30):
            link = Link.objects.create( #pyright: ignore
                code=faker.pystr(min_chars=6, max_chars=6), 
                user=users[i % len(users)]
            )
            link.products.add(products[i % len(products)])

        self.stdout.write(self.style.SUCCESS("🌱 Seeding has been completed")) #pyright: ignore
