from rest_framework import serializers
from core.models import Link, Product, User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName', 'email', 'username', 'password', 'is_ambassador']
        extra_kwargs = {
            'password': {'write_only': True}
        }    

class LinkSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = Link
        fields = "__all__"


