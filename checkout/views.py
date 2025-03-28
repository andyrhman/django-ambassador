from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from checkout.serializers import LinkSerializer #pyright: ignore
from core.models import Link, Order, OrderItem, Product
import decimal
# Create your views here.

class LinkAPIView(APIView):

    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()  # pyright: ignore
        serializer = LinkSerializer(link)
        return Response(serializer.data)

class OrderAPIView(APIView):
    def post(self, request):
        data = request.data

        link = Link.objects.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException("Invalid Code!")

        order = Order()
        order.user = link.user
        order.code = link.code
        order.ambassador_email = link.user.email
        order.fullName = data['fullName']
        order.email = data['email']
        order.address = data['address']
        order.country = data['country']
        order.city = data['city']
        order.zip = data['zip']
        order.save()

        for item in data["products"]:
            product = Product.objects.filter(pk=item["product_id"]).first()
            quantity = decimal.Decimal(item['quantity'])
            
            orderItem = OrderItem()
            orderItem.order = order
            orderItem.product_title = product.title
            orderItem.price = product.price 
            orderItem.quantity = quantity
            orderItem.ambassador_revenue = (
                decimal.Decimal('0.1') *
                decimal.Decimal(str(product.price)) *
                quantity
            )
            orderItem.admin_revenue =  (
                decimal.Decimal('0.1') *
                decimal.Decimal(str(product.price)) *
                quantity
            )
            orderItem.save()

        return Response({"message": "Success"})
