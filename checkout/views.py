from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from checkout.serializers import LinkSerializer #pyright: ignore
from core.models import Link, Order, OrderItem, Product
import decimal
from django.db import transaction
import stripe
import traceback
from django.core.mail import send_mail
from decouple import config
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
            order.links = link
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
                
                order_item = OrderItem()
                order_item.order = order
                order_item.product_title = product.title
                order_item.price = product.price 
                order_item.quantity = quantity
                order_item.ambassador_revenue = (
                    decimal.Decimal('0.1') *
                    decimal.Decimal(str(product.price)) *
                    quantity
                )
                order_item.admin_revenue =  (
                    decimal.Decimal('0.1') *
                    decimal.Decimal(str(product.price)) *
                    quantity
                )
                order_item.save()

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

            stripe.api_key = config('STRIPE_SECRET_KEY')

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

class OrderConfirmAPIView(APIView):
    def post(self, request):

        order = Order.objects.filter(transaction_id=request.data['source']).first()
        if not order:
            raise exceptions.APIException('Order not found!')

        order.complete = 1
        order.save()

        # Admin Email
        send_mail(
            subject='An Order has been completed',
            message='Order #' + str(order.id) + 'with a total of Rp' + str(order.admin_revenue) + ' has been completed!',
            from_email='from@email.com',
            recipient_list=['admin@admin.com']
        )

        send_mail(
            subject='An Order has been completed',
            message='You earned Rp' + str(order.ambassador_revenue) + ' from the link #' + order.code,
            from_email='from@email.com',
            recipient_list=[order.ambassador_email]
        )

        return Response({
            'message': 'success'
        })

