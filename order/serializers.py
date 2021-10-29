from rest_framework import serializers
from .models import Cart, Order


class CartSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.name')

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        cart = Cart.objects.create(
            username=request.user,
            **validated_data
        )
        return cart


class OrderSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.name')
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
#    serializer = OrderSerializer(data=request.data)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        # cart = validated_data.pop('cart')
        username = request.user
        order = Order.objects.create(username=username)
        total = cart['rent'].rent * cart['days'].days
        # for item in cart:
        #     total += item['rent'].rent * item['days'].days
        #     Cart.objects.create(
        #         order=order,
        #         rent=item['rent'],
        #         days=item['days']
        #     )
        order.total_sum = total
        order.save()
        return order













    # cart = serializers.SerializerMethodField("get_cart")
    # created_at = serializers.DateTimeField(read_only=True)
    # status = serializers.CharField(read_only=True)
    # username = serializers.ReadOnlyField(source='username.name')
    #
    # def get_cart(self, request):
    #     cart = request.cart.all
    #     return cart
    #
    # class Meta:
    #     model = Order
    #     fields = '__all__'
    #
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     cart = validated_data.pop('cart')
    #     username = request.user
    #     order = Order.objects.create(username=username)
    #     total = 0
    #     for item in cart:
    #         total += item['rent'].rent * item['days'].days
    #         Cart.objects.create(
    #             order=order,
    #             rent=item['rent'],
    #             days=item['days']
    #         )
    #     order.total_sum = total
    #     order.save()
    #     return order
