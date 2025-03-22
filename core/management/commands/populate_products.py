from random import randrange

from django.core.management import BaseCommand
from faker import Faker

from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker("id_ID")

        for _ in range(30):
            seed = faker.uuid4()  # Unique seed for each image
            image_url = f"https://picsum.photos/seed/{seed}/600/400"  # Adjust dimensions as needed

            Product.objects.create(  # pyright: ignore
                title=faker.name(),  # or use a product name from a custom provider
                description=faker.text(),
                price=randrange(200000, 500000),
                image=image_url,
            )

