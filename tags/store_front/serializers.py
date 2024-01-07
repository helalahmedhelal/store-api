from decimal import Decimal
from rest_framework import serializers
from .models import Address, Collection, Customer, Order, Product,review,Cart,CartItem


class CollectionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    product_count=serializers.IntegerField()
    
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title= serializers.CharField(max_length=255)
    slug=serializers.SlugField()
    description=serializers.CharField(max_length=500)
    last_update=serializers.DateTimeField(read_only=True)
    inventory=serializers.IntegerField()
    price=serializers.DecimalField(max_digits=6,decimal_places=2,coerce_to_string=False,source='unit_price')
    pricewithtax=serializers.SerializerMethodField(method_name='taxes')
    collection=serializers.StringRelatedField()
    #collection=serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), view_name='collection-detail')
    def taxes(self,product:Product): 
       return product.unit_price*Decimal(1.1)
  
  
   
#  CustomerSerializer class
class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']
    
       
#   AddresSerializer class     
class AddresSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address 
        fields=['street','city','customer']    
    customer=CustomerSerializer()    
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['placed_at','payment_status','customer']
    customer=CustomerSerializer()            
 
 
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= review
        fields=['product','name','description','date']
                
    def create(self, validated_data):
        product_id=self.context['product_id']
        
        return review.objects.create(product_id=product_id,**validated_data)    
        
############################################################################################
#cart serializer
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['title','unit_price']  
        
class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSimpleSerializer()
    price=serializers.SerializerMethodField(method_name='total_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','price']

    def total_price(self,cartitem:CartItem):
        return cartitem.product.unit_price*cartitem.quantity    
            
       
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    id=serializers.IntegerField(read_only=True)
    cart_total_price=serializers.SerializerMethodField(method_name='total_price')
    class Meta:
        model=Cart
        fields=['id','created_at','items','cart_total_price']        
    def total_price(self,cart:Cart):
        t=0
        for c in cart.items.all():
            t=t+(c.quantity*c.product.unit_price)
        return t        

        
        
        
        
        
        