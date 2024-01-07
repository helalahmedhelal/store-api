from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from store_front.serializers import ProductSerializer,CollectionSerializer,CartItemSerializer,CartSerializer,AddresSerializer,ReviewSerializer,CustomerSerializer,OrderSerializer
from .models import Address, Collection, Customer, Order, Product,OrderItem,review,Cart,CartItem
from django.db.models.aggregates import Avg,Count,Sum,Min,Max
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_204_NO_CONTENT
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
#################################################################################################################          
@api_view()
def productlist(request):
        queryset=Product.objects.select_related('collection').all().order_by('id')
        productsdata= ProductSerializer(queryset,many=True,context={'request': request})
        return Response(productsdata.data)
    

@api_view(['GET','POST'])
def productdetails(request,id):
    if request.method== 'GET':
        product=get_object_or_404(Product,pk=id)
        productdata=ProductSerializer(product,context={'request': request})
        return Response(productdata.data)
    elif request.method== 'POST':
        productpost=ProductSerializer(data=request.data)
        productpost.is_valid(raise_exception=True)
        productpost.validated_data
        productpost.save()
        return Response('ok')


#############collection views    
@api_view()
def collectiondata(request):
    collection=Collection.objects.annotate(product_count=Count('product')).all()
    collectiondata=CollectionSerializer(collection,many=True)
    return Response(collectiondata.data)

@api_view()
def collectiondetail(request,pk):
    collection=Collection.objects.annotate(product_count=Count('product')).get(id=pk) 
    collectiondata=CollectionSerializer(collection)
    return Response(collectiondata.data)


####################################################################################################
@api_view()
def addressdetails(request):
    address=Address.objects.select_related('customer').all()
    addressdata=AddresSerializer(address,many=True) 
    return Response(addressdata.data)      



@api_view()
def customerlist(request):
    queryset=Customer.objects.annotate(order_count=Count('order')).all()
    customerserializer=CustomerSerializer(queryset,many=True)
    return Response(customerserializer.data)


@api_view()
def orderlist(request):
    queryset=Order.objects.select_related('customer').all()
    orderserializer=OrderSerializer(queryset,many=True)
    return Response(orderserializer.data)

###########################################################################################
#######################################################################################################








#customer views
@api_view(['GET','POST'])
def customerdata(request,id):
    if request.method == 'GET':
        queryset=get_object_or_404(Customer ,id=id)
        customerSerializer = CustomerSerializer(queryset)
        return Response(customerSerializer.data)
    elif request.method == 'POST':
        customerpost=CustomerSerializer(data=request.data)
        customerpost.is_valid(raise_exception=True)
        customerpost.save()
        return Response(customerpost.data,status=HTTP_201_CREATED)






class CustomerView(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer 
    permission_classes=[IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
           return  [AllowAny()]
        
        return [IsAuthenticated()]
        
    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        customer=Customer.objects.get(user_id = request.user.id)
        
        if request.method == 'GET':
           serializer=CustomerSerializer(customer)
           return Response(serializer.data) 
        elif request.method == 'PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
     
     
     
     
     
#######################################################################################################        
#####################################################################################################  








  
@api_view(['GET','PUT','DELETE'])
def customerdataupdate(request,id):
    queryset=Customer.objects.annotate(order_count=Count('order')).get(pk=id)
    if request.method == 'GET':
        customerSerializer = CustomerSerializer(queryset)
        return Response(customerSerializer.data)
    elif request.method == 'PUT':
        customerpost=CustomerSerializer(queryset,data=request.data)
        customerpost.is_valid(raise_exception=True)
        customerpost.save()
        return Response(customerpost.data,status=HTTP_201_CREATED)    
    elif request.method=='DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
 
 
 
 
 
 
 
 
 
    
################################################################################################################
####### class based views for product




class ProductDetailsClass(APIView):
    def get(self,request):
          product= Product.objects.all() 
          productdata=ProductSerializer(product,many=True,context={'request': request})
          return Response(productdata.data)  
  
      
class ProductGenericClass(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.all().select_related('collection')
    def get_serializer_class(self):
        return ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}

class ProductGenericClassGet(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    def delete(self, request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0:
           return Response({'error':'can not delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED,)
        else: 
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        






        
############################################################################################################
#product with view sets 


       
class productViewset(ModelViewSet):
    queryset=Product.objects.select_related('collection').all()
    serializer_class=ProductSerializer
    permission_classes=[IsAdminOrReadOnly]
    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
           return Response({'error':'can not delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED,)
        else:   
           return super().destroy(request, *args, **kwargs)
    

class productViewsetfilter(ModelViewSet):
    queryset=Product.objects.select_related('collection').all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
           return Response({'error':'can not delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED,)
        else:   
           return super().destroy(request, *args, **kwargs)











#######################################################################################


class review_viewset(ModelViewSet):
    def get_queryset(self):
        return review.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class=ReviewSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}



##############################################################################################################





@api_view(['GET','POST'])
def cart_detail(request,id):
    if request.method== 'GET':
        cart=get_object_or_404(Cart,pk=id)
        carttdata=CartSerializer(cart)
        return Response(carttdata.data)
    elif request.method== 'POST':
        cartpost=CartSerializer(data=request.data)
        cartpost.is_valid(raise_exception=True)
        cartpost.save()
        return Response('ok')


class CartViewset(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
      queryset=Cart.objects.all()
      serializer_class=CartSerializer

class CartItemViewset(ModelViewSet):
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    serializer_class=CartItemSerializer











































