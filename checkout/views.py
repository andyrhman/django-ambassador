from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from checkout.serializers import LinkSerializer #pyright: ignore
from core.models import Link, Order, OrderItem, Product
import decimal
from django.db import transaction
import stripe
import traceback
# Create your views here.

class LinkAPIView(APIView):

    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)

class OrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data

        link = Link.objects.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException("Invalid Code!")
        try:
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

            line_items = []
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

                line_items.append({
                    'price_data': {
                        'currency': 'idr',
                        'unit_amount': int(product.price),
                        'product_data': {
                            'name': product.title,
                            'description': product.description,
                            'images': [
                                product.image
                            ],
                        },
                    },
                    'quantity': quantity
                })

            stripe.api_key = 'sk_test_51R7vO3D150d1kLQ1GVFsvNxiFpJKq10Lb6U00zS1E8xqxx1eawEmGpjUEXDL3vCPmPJzZ7pg7entzuZDtcJtXZCI0007AwHd8T'

            source = stripe.checkout.Session.create(
                success_url='http://localhost:5000/success?source={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:5000/error',
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment'
            )

            order.transaction_id = source['id']
            order.save()

            return Response(source)

        except Exception:
           traceback.print_exc()
           transaction.rollback()
        
        return Response({"message": "Success"})
