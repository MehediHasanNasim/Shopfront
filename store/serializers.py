from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from .models import *
from .import views

'''model serializer'''
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


'''Serializer'''
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


'''model serializer'''

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
    
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection', 'images']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
            
        except CartItem.DoesNotExist: 
            CartItem.objects.create(cart_id=cart_id, **self.validated_data)
    
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerilizer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerilizer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        cart_id = serializers.UUIDField()
        
        def validate_cart_id(self, cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError('No cart with the given Id was found...')
            
            if CartItem.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('The cart is empty')
            return cart_id
        
        def save(self, **kwargs):
            
            cart_id = self.validated_data['cart_id']
            
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            
            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)
            
            order_items = [
                OrderItem(
                    order = order, 
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()
            
            order_created.send_robust(self.__class__, order=order)
            
            return order 
        
        
        

''' validation example'''
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password do not match')
    #     return data
    

'''Serializer'''
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name = 'collection-detail',
#     )
    # # For whole of the fields
    # collection = CollectionSerializer()

    # # For Specific field
    # collection = serializers.StringRelatedField()
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # def calculate_tax(self, product: Product):
    #     return product.unit_price * Decimal(1.1)
    
    # price = serializers.DecimalField(coerce_to_string=False)

