from django.shortcuts import render
from .serializers import *
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import exceptions
from rest_framework import authentication
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView


class UserAuthView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


class CustomerAPIView(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    authentication_classes = [TokenAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class ProductAPIView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    authentication_classes = [TokenAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class OrderAPIView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    authentication_classes = [TokenAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["id"]
    search_fields = ["customer", " date_ordered"]


class OrderItemAPIView(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    authentication_classes = [TokenAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["product"]
    search_fields = ["product"]


class ShippingAddressAPIView(ModelViewSet):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()

    authentication_classes = [TokenAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["address"]
    search_fields = ["address", "city", "state", "zipcode"]
