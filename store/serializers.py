from decimal import Decimal
from rest_framework import serializers
from .models import *
from .import views

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name = 'collection-detail',
    )
    # # For whole of the fields
    # collection = CollectionSerializer()

    # # For Specific field
    # collection = serializers.StringRelatedField()
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # price = serializers.DecimalField(coerce_to_string=False)

