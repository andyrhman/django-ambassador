import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# ! Fixing the migration problem if there is unknown error
# ? https://chat.openai.com/c/a2bedf2d-801d-4814-8298-9dd7fb0973c3
"""
TLDR;
Delete the migrations file, drop the tables, and do this
python manage.py flush
python manage.py makemigrations your_app_name
python manage.py migrate
"""

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_ambassador = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_ambassador = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    fullName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_ambassador = models.BooleanField(default=True)  # pyright: ignore[reportArgumentType]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = None
    last_name = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # Ensures email is prompted when creating superuser

    objects = UserManager()

    # @property
    # def name(self):
    #     return self.first_name + ' ' + self.last_name

    @property
    def revenue(self):
        orders = Order.objects.filter(user_id=self.pk, complete=True) #pyright: ignore
        return sum(o.ambassador_revenue for o in orders)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)
    price = models.FloatField()
    image = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Link(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    transaction_id = models.CharField(max_length=255, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    links = models.ForeignKey(Link, null=True, on_delete=models.SET_NULL, related_name="orders") # finding the nested orders for link serializers
    code = models.CharField(max_length=255)
    ambassador_email = models.CharField(max_length=255)
    fullName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    complete = models.BooleanField(default=False) #pyright: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def name(self):
    #     return self.first_name + ' ' + self.last_name

    @property
    def ambassador_revenue(self):
        items = OrderItem.objects.filter(order_id=self.pk) #pyright: ignore
        return sum(i.ambassador_revenue for i in items)

    @property
    def admin_revenue(self):
        items = OrderItem.objects.filter(order_id=self.pk) #pyright: ignore
        return sum(i.admin_revenue for i in items)

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product_title = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    admin_revenue = models.FloatField()
    ambassador_revenue = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


