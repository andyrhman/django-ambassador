from random import randint
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Link, Order, OrderItem, User  

class Command(BaseCommand):
    help = "Seed orders and order items data"

    def handle(self, *args, **kwargs):
        faker = Faker("id_ID")
        users = list(User.objects.all())
        links = Link.objects.all() #pyright: ignore

        for i in range(30):
            link = links[i % len(links)]
            order = Order.objects.create( #pyright: ignore
                code=link.code,
                ambassador_email=faker.email(),
                user=users[i % len(users)],  
                fullName=faker.name(),  
                email=faker.email(),
                address=faker.street_address(),
                country=faker.country(),
                city=faker.city(),
                zip=faker.postcode(),  
                complete=True
            )

            for _ in range(randint(1, 4)):
                OrderItem.objects.create( #pyright: ignore
                    order=order,
                    product_title=faker.word(),  
                    price=randint(100000, 5000000),
                    quantity=randint(1, 4),
                    ambassador_revenue=randint(10000, 500000),
                    admin_revenue=randint(1000, 50000)
                )

        self.stdout.write(self.style.SUCCESS("🌱 Seeding has been completed")) #pyright: ignore

