from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('customerview',views.CustomerView)
router.register('productsviewset',views.productViewset)
products_router=routers.NestedDefaultRouter(router,'productsviewset',lookup='product')
products_router.register('review',views.review_viewset,basename='product-reviews')



urlpatterns = [
    ######################################################################################################
    #router for view set
    path(r'',include(router.urls)),
    path(r'',include(products_router.urls)),
    
    
    ######################################################################################################
    
    path('products',views.productlist),
    path('product/<id>',views.productdetails),
    
    
    path('collection/<pk>',views.collectiondetail,name='collection-detail'),
    path('collectiondata',views.collectiondata),
    
    
    
    
    path('address',views.addressdetails),
    path('productgetclass',views.ProductDetailsClass.as_view()),
    
    ######################################################################################################
    #customer routes
    path('customerlist',views.customerlist),
    path('customerdata/<id>',views.customerdata),
    #path('customerview',views.CustomerView.as_view()),
    
    
    ########################################################################################################
    path('orderlist',views.orderlist),
    
    
    
    path('productgeniric',views.ProductGenericClass.as_view()),
    path('productget/<pk>',views.ProductGenericClassGet.as_view()),
    ########################################################################
    
    
    #cart routes
    path('cartdetail/<id>',views.cart_detail),
    
    
]
