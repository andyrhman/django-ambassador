from rest_framework import serializers

from core.models import Link, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField("get_total")

    def get_total(self, obj):
        items = OrderItem.objects.filter(order_id=obj.id) #pyright: ignore
        return sum((o.price * o.quantity) for o in items)

    class Meta:
        model = Order
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    lynkx = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Link
        fields = "__all__"
