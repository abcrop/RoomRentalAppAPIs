"""
Acutal endpoints for outer domain to communicate with this application,
apis.py only talks with serializers.py and services.py
"""
import logging
import re
import requests
import os
import dotenv
import json
from django.db.models import signals as django_signals
from endpoints import signals
from django.core.validators import validate_email
from endpoints.services import validate_password, validate_username
from django.utils.functional import partition
from django.views.generic.base import View
from rest_framework.serializers import raise_errors_on_nested_writes
from endpoints import constants
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest, ValidationError
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied, bad_request
from rest_framework.response import Response
from rest_framework import status
from endpoints import serializers
from endpoints import models
from django.contrib.auth.decorators import login_required
from endpoints import permissions
from endpoints.permissions import IsAdminOrLandLordAndReadOnly, IsAdminOrTenantAndReadOnly, IsAdminOrResourceOwnerOnly, IsAdminAndReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from endpoints import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.contrib.auth.hashers import check_password, make_password
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider import models as oauth2Model

"""
Configuring logger
"""
logger = logging.getLogger(__name__)
del logging

"""
Configuring dotenv to get client_secret client_id
"""
dotenv_file = dotenv.find_dotenv(filename='.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

"""
-First needed to signup as Gharbeti
-Only Gharbeti people can post/put/delete
"""
class HouseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HouseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandLordAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ('owner_id', )
    
    def get_queryset(self):
        queryset = models.House.objects.all()
        return queryset

"""
-First needed to signup as Gharbeti
-Only Gharbeti with his/her room can add feature to their room
"""
class FeatureViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeatureSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandLordAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ('room_id', )
    
    
    def get_queryset(self):
        queryset = models.Feature.objects.all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        # if request.user.id != 1:
        #     only_owner_queryset = queryset.filter(room_id__owner_id=request.user.id)
            
        #     page = self.paginate_queryset(only_owner_queryset)
        #     if page is not None:
        #         serializer = self.get_serializer(page, many=True)
        #         return self.get_paginated_response(serializer.data)
            
        return super().list(request,*args,**kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        # serialized_data = serializer.data
        # room_id = serialized_data['room_id']
        # room = models.Room.objects.get(id=room_id)
        # owner_id = room.owner_id.id
        
        # if request.user.id != owner_id:
        #     raise PermissionDenied() 
                
        return super().create(request, *args, **kwargs)
        
    
"""
- First needed to signup as Gharbeti to add a room
- 5 functionality: GET, POST, PUT, DELETE, PATCH
- Offers methods: list, create, retrieve, update, partial_update, destroy
"""
class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandLordAndReadOnly,]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = filters.RoomFilter
    search_fields = ('room_name', 'house_id__location')
    ordering_fields = ('room_name', 'room_price', 'category_id', )
    
    """ 
    filterset_class and filterset_fields can't come together
    """
    # filterset_fields = ('category_id','room_price',)
    
    """
    Only these methods allowed
    """
    # http_method_names  = ['get']
    
    def get_queryset(self):
        querset = models.Room.objects.all()
        order_by = self.request.query_params.get('order_by', '')
        
        if order_by:
            order_by_name = order_by.split(" ")[1]
            order_by_sign = order_by.split(" ")[0]

            logger.debug(order_by_sign)

            order_by_sign = '' if order_by_sign == 'asc' else '-'
            logger.debug(order_by_name)
            logger.debug(order_by_sign)
            
            querset = querset.order_by(order_by_sign + order_by_name)
        print("hello world")
        return querset
    
    # def get_permissions(self):
    #     if self.action == 'list':
    #         self.permission_classes = [AllowAny,]
    #     else:
    #         self.permission_classes = [IsAuthenticated,]
            
    #     return super().get_permissions()
    
    #Caching: cache requested url for each user for 2 hours
    # @method_decorator(cache_page(60*60*2))
    # #With auth
    # @method_decorator(vary_on_headers('authorization',))
    def list(self, request):
        queryset = self.get_queryset()
        
        return super().list(self,request)
        
    #PostRequest
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #calls serializer.save()->calls create() in serializers
        #and we don't even need to readd ownerid(foreignkey) manually
        self.perform_create(serializer)
        #on successful post request, returns location headers in response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers= headers)

class RoomRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTenantAndReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ('tenant_id', 'room_id', 'is_accepted', 'created_at',)
         
    def get_queryset(self):
        queryset = models.RoomRequest.objects.all()
        return queryset
    
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTenantAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ('room_id', 'tenant_id', 'created_at', )
    
    def get_queryset(self):
        queryset = models.Favorite.objects.all()
        return queryset
    

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminAndReadOnly, ]
    filter_backends = [SearchFilter, ]
    search_fields = ('category_name', )
    
    def get_queryset(self):
        queryset = models.Category.objects.all()
        return queryset

class RentalDataViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RentalDataSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTenantAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_class = filters.RentalDataFilter
    search_fields = ('last_paid_date', 'next_payable_date', 'advance_paid_date', 'room_id__house_id__location', )
    ordering_fields = ('rating', 'next_payable_rent', 'advance_rent', 'rent_till_now', )
    
    
    def get_queryset(self):
        queryset = models.RentalData.objects.all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if request.user.user_type != 'AD':
            tenant_only_queryset = queryset.filter(id=request.user.id)
            page = self.paginate_queryset(tenant_only_queryset)
            serializer = self.get_serializer(data=page, many=True)
            
            return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)
        
        return super().list(request, *args, **kwargs)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTenantAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    filterset_fields = ('room_id', 'tenant_id', 'created_at', )
    search_fields = ('room_id__house_id__location', 'room_id__room_name', )
    
    def get_queryset(self):
        queryset = models.Favorite.objects.all()
        return queryset

class RewardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RewardSerializer
    permission_classes = [IsAuthenticated, IsAdminAndReadOnly, ]
    
    def get_queryset(self):
        queryset = models.Reward.objects.all()
        return queryset

class RewardTrackerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RewardTrackerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTenantAndReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ('rentalData_id', 'reward_id', )
    search_fields = ('created_at', 'rentalData_id__tenant_id__first_name', 'rentalData_id__tenant_id__phone_number', 'rentalData_id__tenant_id__email', 'rentalData_id__rental_id__owner_id__email')
    ordering_fields = ('created_at', 'rentalData_id', 'reward_id', )
    
    def get_queryset(self):
        queryset = models.RewardTracker.objects.all()
        return queryset

class SignupUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SignupUserSerializer
    http_method_names = ['post',]
    permission_classes = [ ]
    
    def get_queryset(self):
        queryset = models.AppUser.objects.all()
        return queryset
        
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     if request.user.user_type != 'AD':
    #         only_owner_queryset = queryset.filter(id=request.user.id)
    #         serializer = self.get_serializer(only_owner_queryset, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
        
    #     return super().list(request, *args, **kwargs)

class UsersViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = [IsAuthenticated, ]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        """
        Removing admin from queryset
        """
        if request.user.user_type != 'AD':
            only_admin_queryset = queryset.filter(user_type='AD')
            admin_ids = [admin.id for admin in only_admin_queryset]
            except_admin_queryset = queryset.exclude(id__in = admin_ids)
            page = self.paginate_queryset(except_admin_queryset)
            
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)
                            
        return super().list(request, *args, **kwargs)
        
    
"""
Params: current_password, password
"""
class UpdatePassword(mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.PasswordUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrResourceOwnerOnly,]
    http_method_names = ('put',)
    
    # def retrieve(self, request, *args, **kwargs):
    #     user = self.queryset.get(id=self.kwargs['pk'])
    #     return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        user = self.queryset.get(id=self.kwargs['pk'])
        
        if check_password(data['current_password'], encoded = user.password):
            """
            Partial=False in Serializer, told Update mixins to use PUT not PATCH
            """
            serializer = self.get_serializer(self.get_object(),data=data, partial=False)
            if(serializer.is_valid(raise_exception = True)):
                with transaction.atomic(savepoint=False):
                    """
                    Refreshing the access token
                    """
                    current_refresh_token = request.data['refresh_token']
                    if not current_refresh_token: 
                        return BadRequest() 
                    
                    print(f"refresh token: {current_refresh_token}")
                    
                    result = requests.post(
                        constants.BASEURL+"/refreshToken/",
                        data={
                            'refresh_token': current_refresh_token,        
                        },
                        )
                    
                    if result.status_code == 200:
                        user.set_password(serializer.validated_data['new_password'])
                        user.save()
                    
                        return Response(result.json())        
                        
                    return Response({'message': 'Internal server error'}, status=result.status_code)        
                    
            return Response({'message': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)        
        
        return Response({'message': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)        
    
"""
Params: first_name, last_name, username, image, education, occupation, user_type,
"""
class UpdateUser(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrResourceOwnerOnly, ]
    http_method_names = ('get', 'patch', )
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class DeleteUser(mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.UserDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrResourceOwnerOnly, ]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class GetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.GetTokenSerializer
    permission_classes = (AllowAny, )
    http_method_names = ('post',)
    data = {}
    schema = None

    def bad_params(self):
        """
        Restricting number of parameters users can put.
        """
        
        if len(self.request.data) > constants.NUMBER_OF_LOGIN_PARAMERTERS or len(self.request.data) < constants.NUMBER_OF_LOGIN_PARAMERTERS:
            self.data['error'] = "Bad parameters."
            return Response(self.data, status=constants.INVALID_PARAMETERS)    
        
    def create(self, request, *args, **kwargs):    
        url = constants.BASEURL+f"/oauth2/token{os.environ['GETTOKEN']}/"
        
        grant_type = 'password'
        client_id = os.environ.get('CLIENT_ID_MOBILE_CLIENT')
        client_secret = os.environ.get('CLIENT_SECRET_MOBILE_CLIENT')
        
        try:
            username = request.data['username']
            password = request.data['password']
            
            self.bad_params()
            username = validate_username(self, username)
            password = validate_password(self, password)
            
            data = {
                'grant_type' : grant_type,
                'username' : username,
                'password' : password,
                'client_id' : client_id,
                'client_secret': client_secret
            }

            print(username , password)
            result = requests.post(url, data=data)
            
            if result.status_code == 200:
                print(result.text)
                return Response(result.json())
            
            elif result.status_code == 401:
                self.data['error'] = "Invalid client."
                
            elif result.status_code == 400:
                self.data['error'] = "Username or password is incorrect."
            
            else:
                self.data['error'] = "Error while getting token."
            print(result.text)
            return Response(data=self.data, status=result.status_code)
                
            
        except Exception as e:
            self.data['error'] = "Username and password are required."
            return Response(self.data, status=status.HTTP_400_BAD_REQUEST)
        
       

class RevokeTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.RevokeTokenSerializer
    permission_classes = [IsAuthenticated, IsAdminOrResourceOwnerOnly, ]
    data = {}
    schema = None
    
    def create(self, request, *args, **kwargs):
        url = constants.BASEURL + f"/oauth2/revoke_token{os.environ['REVOKETOKEN']}/"
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        client_id = os.environ.get('CLIENT_ID_MOBILE_CLIENT')
        client_secret = os.environ.get('CLIENT_SECRET_MOBILE_CLIENT')
        print(token)
        data = {
            'token' : token,
            'client_id' : client_id,
            'client_secret': client_secret,
        }
        previous_refresh_token = oauth2Model.RefreshToken.objects.get(access_token__token=token)
        result = requests.post(url, data=data,)
        
        if(result.status_code == 200):
            previous_refresh_token.delete()
            self.data['success'] = "Access token is successfully revoked."
            return Response(data= self.data, status = status.HTTP_204_NO_CONTENT)
        
        elif result.status_code == 401:
            self.data['message'] = "Invalid client."
            
        elif result.status_code == 400:
            self.data['message'] = "Invalid token."
            
        else:
            self.data['message'] = "Error revoking access token."
        return Response(data= self.data, status = result.status_code)

"""
RefreshTokenViewSet:
Params: refresh_token
-Basically, it deletes previous refresh_token which is of no use
then updates it's related access_token

"""
class RefreshTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.RefreshTokenSerializer
    permission_classes = ()
    data = {}
    schema = None
    
    def create(self, request, *args, **kwargs):
        url = constants.BASEURL + f"/oauth2/refresh_token{os.environ['REFRESHTOKEN']}/"
        grant_type = 'refresh_token'
        refresh_token = request.data['refresh_token']
        client_id = os.environ.get('CLIENT_ID_MOBILE_CLIENT')
        client_secret = os.environ.get('CLIENT_SECRET_MOBILE_CLIENT')
        
        data = {
            'grant_type' : grant_type,
            'client_id' : client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }

        result = requests.post(url, data=data,)
        print(result.status_code)
        
        if result.status_code == 200:
            oauth2Model.RefreshToken.objects.get(token = refresh_token).delete()
            print(result)
            return Response(result.json())
        
        elif result.status_code == 401:
            self.data['message'] = "Invalid client."
            
        elif result.status_code == 400:
            self.data['message'] = "Invalid refresh token."
        
        else:
            self.data['message'] = "Error while refreshing access token."
        return Response(data = self.data, status = result.status_code)

@login_required()
@api_view(['GET'])
def Home(request):
    data = {
        'message': 'Grettings, Welcome to the Room Rental APIs.',
        'user_type': request.user.user_type,
    }
    return Response(data=data, status=status.HTTP_200_OK)
    
"""
Dummy RoomRequest
-to demonstrate custom json output
"""      
# class RoomRequest(generics.GenericAPIView):
#     serializer_class = serializers.RoomRequestSerializer
    
#     def post(self,request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         data = {}
        
#         if serializer.is_valid():
#             data = serializer.data
#             data['is_valid'] = True
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             data['is_valid'] = False
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
#     def get(self, request, *args, **kwargs):
#         return Response({'luck':"GoodLuck",}, status=status.HTTP_201_CREATED)
      
# @login_required()
# @api_view(['POST'])
# def room_reqeust(request):
#     serializer = serializers.RoomRequestSerializer(data=request.data)
#     data = {}
    
#     if serializer.is_valid():
#         data = serializer.data
#         data['is_valid'] = True
#         return Response(data, status=status.HTTP_201_CREATED)
#     else:
#         data['is_valid'] = False
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)  
    