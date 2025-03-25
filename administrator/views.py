from rest_framework import exceptions, generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from administrator.serializers import (  # pyright: ignore
    LinkSerializer,
    OrderSerializer,
    ProductSerializer,
)
from common.authentication import JWTAuthentication
from common.serializers import UserSerializer
from core.models import Link, Order, Product, User
from django.core.cache import cache

# Create your views here.
class AmbassadorsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)

        return Response(UserSerializer(ambassadors, many=True).data)


class ProductGenericAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by("-updated_at")  # pyright: ignore
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        try:
            response = self.create(request)

            for key in cache.keys('*'):
                if 'producs_frontend' in key:
                    cache.delete(key)

            cache.delete('products_backend')
            return response

        except exceptions.ValidationError as e:
            # Generate a more user-friendly message that includes the field name
            errors = {key: value[0] for key, value in e.detail.items()}  # pyright: ignore
            first_field = next(iter(errors))
            field_name = first_field.replace("_", " ").capitalize()
            if "required" in errors[first_field]:
                message = f"{field_name} is required."
            else:
                message = f"{field_name} error: {errors[first_field]}"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        for key in cache.keys('*'):
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response

    def delete(self, request, pk=None):
        response = self.destroy(request, pk)
        for key in cache.keys('*'):
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response

class LinkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)  # pyright: ignore
        serializer = LinkSerializer(links, many=True)

        return Response(serializer.data)


class OrderApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        orders = Order.objects.filter(complete=True)  # pyright: ignore
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)
