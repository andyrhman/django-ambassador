import math
import time
import string
import random
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ambassador.serializers import ProductSerializer, LinkSerializer
from common.authentication import JWTAuthentication
from core.models import Product, Link, Order
from rest_framework import exceptions, status
from django_redis import get_redis_connection
from faker import Faker
# Create your views here.


class ProductFrontendAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2, key_prefix="products_frontend"))
    def get(self, _):
        time.sleep(2)
        products = Product.objects.all()  # pyright: ignore
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductBackendAPIView(APIView):
    def get(self, request):
        products = cache.get("products_backend")
        if not products:
            time.sleep(2)
            products = list(Product.objects.all())  # pyright: ignore
            cache.set("products_backend", products, timeout=60 * 30)  # 30 min

        s = request.query_params.get("search", "")
        if s:
            products = list(
                [
                    p
                    for p in products
                    if (s.lower() in p.title.lower())
                    or (s.lower() in p.description.lower())
                ]
            )

        total = len(products)

        sort = request.query_params.get("sort", None)
        if sort == "asc":
            products.sort(key=lambda p: p.price, reverse=True)
        elif sort == "desc":
            products.sort(key=lambda p: p.price)

        per_page = 9
        page = int(request.query_params.get("page", 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = ProductSerializer(products[start:end], many=True).data
        return Response(
            {
                "data": data,
                "meta": {
                    "total": total,
                    "page": page,
                    "last_page": math.ceil(total / per_page),
                },
            }
        )

class LinkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        try:
            faker = Faker("id_ID")
            user = request.user

            serializer = LinkSerializer(
                data={
                    "user": user.id,
                    "code": faker.pystr(min_chars=6, max_chars=6), 
                    "products": request.data["products"],
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        except exceptions.ValidationError as e:
            # Check if e.detail is a dict, otherwise default to a string message
            if isinstance(e.detail, dict):
                errors = {key: value[0] for key, value in e.detail.items()}
                first_field = next(iter(errors))
                field_name = first_field.replace("_", " ").capitalize()
                if "already exists" in errors[first_field]:
                    message = f"{field_name} already exists."
                else:
                    message = f"{field_name} error: {errors[first_field]}"
            else:
                message = str(e.detail)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

class StatsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        links = Link.objects.filter(user_id=user.id) #pyright: ignore

        return Response([self.format(link) for link in links])

    def format(self, link):
        orders = Order.objects.filter(code=link.code, complete=1) #pyright: ignore

        return {
            'code': link.code,
            'count': len(orders),
            'revenue': sum(o.ambassador_revenue for o in orders)
        }

class RankingsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        con = get_redis_connection("default")

        rankings = con.zrevrangebyscore('rankings', min=0, max=10000, withscores=True)

        return Response({
            r[0].decode("utf-8"): r[1] for r in rankings
        })
