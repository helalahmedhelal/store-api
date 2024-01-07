from django.forms import DecimalField, FloatField
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F,Value,  Func, ExpressionWrapper
from store_front.models import Product, OrderItem, Order, Customer
from django.db.models.aggregates import Avg,Count,Sum,Min,Max
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TagetItem

def render_html(request):
    
    content_type=ContentType.objects.get_for_model(Product)
    querset=TagetItem.objects.select_related('tag').filter(content_type=content_type,object_id=8)
    return render(request,'hello.html',{'products':(querset)})

def render_html_get(request):
    queryset=Product.objects.get(pk=1)
    return render(request,'hello.html',{'productpk':queryset})

def get_ordered_items(request):
     querset=Product.objects.filter(id__in= OrderItem.objects.values('product_id') ) 
     return render(request,'hello.html',{'products':list(querset)})


def ORM():
    
    querset= Product.objects.all()
    #we use it to  get spacific object with primary key, pk is lookup parametar
    product=Product.objects.get(pk=1)
    
    #if query set is empty it will return NONE not error
    queryset=Product.objects.filter(pk=0).first()
    
    # return boolean 
    queryset=Product.objects.filter(pk=0).exists()
    
    #query set api field lookup to get price in range (20,30)
    queryset=Product.objects.filter(unit_price__range=(20,30))
    
    #query set api field lookup to get price greter than or eqal 20 
    queryset=Product.objects.filter(unit_price__gte=20)
    
    #query set api field lookup to get description starts with and another lookup contains
    queryset=Product.objects.filter(description__startswith__contains=('Coffe','1'))
    
    #query set api field lookup to filter unit price and last_update by year combiend with and operator
    queryset=Product.objects.filter(unit_price__lte=20, last_update__year=2012)
    
    #query set api field lookup to filter unit price and last_update by year combiend with and operator
    queryset=Product.objects.filter(unit_price__lte=20).filter(last_update__year=2012)
    
    
    #query set api field lookup to filter unit price and last_update by year combiend with or operator using Q object
    queryset=Product.objects.filter(Q(unit_price__lte=20) | Q(last_update__year=2012))
    
    #query set api field lookup to filter unit price and last_update by year combiend with and operator using Q object
    queryset=Product.objects.filter(Q(unit_price__lte=20) & ~Q(last_update__year=2012))
    
    #refrancing oblect with F so we can compare with two two fields
    queryset=Product.objects.filter(unit_price= F('last_update') )
    
    
    queryset=Product.objects.order_by('unit_price')
    queryset=Product.objects.order_by('-unit_price')
    
    #same query choose first element in queryset
    queryset=Product.objects.order_by('unit_price')[0]
    queryset=Product.objects.earliest('unit_price')
    # latest element after des order
    queryset=Product.objects.latest('unit_price')
    
    #limiting and limiting with offset
    querset= Product.objects.all()[:5]
    querset= Product.objects.all()[5:20]
    
    #selecting fields to query but use only sometimes make problems
    querset= Product.objects.values('id','title')
    # when we select attribute not in quered values like 'id', 'title' in template this make (only) send send
    #--> sql requests to fetch the data (video 12 in django ORM is important)
    querset= Product.objects.only('id','title')
    
    #defer make selected field to defered from query
    querset= Product.objects.defer('description')
    
    #selecting fields to query with join another table cant use to compare objects
    querset= Product.objects.values('id','title','collection__title ')
    
    #
    querset=Product.objects.filter(id__in= OrderItem.objects.values('product_id').distinct()).order_by('title')
    
    # create join between one to many relationship tables (video 13 in django ORM is important)
    querset= Product.objects.select_related('collection').all()
    
    #this is not true select_related work only when orderitem is related with collection direct with relation
    queryset=OrderItem.objects.select_related('product').select_related('collection').all()
    # order item not related direct with collection but this query set will work 
    queryset=OrderItem.objects.select_related('product__collection').all()
    # create join between many to many relationship tables (video 13 in django ORM is important)
    querset= Product.objects.prefetch_related('promotions').all()
    
    #aggregation functions 
    result=product.objects.aggregate(Count('id'),Min('unit_price'))
    
    #annotation add addtional field not in data dase (is_new, new_id, is the new field )
    querset=product.objects.annotate(is_new=Value(True))
    querset=product.objects.annotate(new_id=F('id'))
    
    #django functions 
    querset=product.objects.annotate(full_name=Func(F('first_name'),Value(' '),F('last_name'))
                       , function='CONCAT') 
    
    querset=product.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name'))
    
    #groubing data 
    querset=product.objects.annotate(count_orders=Count('order'))
    
    #ExpressionWrapper to make expressions 
    querset=product.objects.annotate(discount=ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField()))
    
    #grouping data by revers relation 
    queryset=Customer.objects.annotate(counter=Count(F('order'))).order_by('-counter').exclude(counter=0)
    
    #quering generic relationships
    def genericrelation(request):
        content_type=ContentType.objects.get_for_model(Product)
        querset=TagetItem.objects.select_related('Tag').filter(content_type=content_type,object_id=1)
        return render(request,'hello.html',{'products':list(querset)}) 
    
    def tagedfrommanger(request):
        TagetItem.objects.get_tags_for_items(Product,1)
        
    def quersetcaching(request):
     querset=Product.objects.filter(id__in= OrderItem.objects.values('product_id')) 
     #in this line evaluating entire querset for best performance
     list(querset)
     querset[:5]
     return render(request,'hello.html',{'products':list(querset)})