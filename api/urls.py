from rest_framework import routers
from .views import *
from django.urls import path, include
from rest_framework.authtoken import views

routers = routers.DefaultRouter()
routers.register(r'customers', CustomerAPIView)
routers.register(r'products', ProductAPIView)
routers.register(r'orders', OrderAPIView)
routers.register(r'orderItem', OrderItemAPIView)
routers.register(r'shippingAddress', ShippingAddressAPIView)

urlpatterns = [

    path('', include(routers.urls)),

]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
