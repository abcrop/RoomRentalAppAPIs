from django.contrib import admin
from django.urls import path
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from endpoints import apis
import dotenv
import os

dotenv_file = dotenv.find_dotenv(filename='.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


#viewset's Routers
router = SimpleRouter()

#room_rental_security
router.register('getToken'+os.environ.get('GETTOKEN'), apis.GetTokenViewSet, "getToken")
router.register('revokeToken'+os.environ.get('REVOKETOKEN'), apis.RevokeTokenViewSet, "revokeToken")
router.register('refreshToken'+os.environ.get('REFRESHTOKEN'), apis.RefreshTokenViewSet, "revokeToken")

#room_rental_resources
router.register('rooms', apis.RoomViewSet, "rooms")
router.register('roomFeatures', apis.FeatureViewSet, "roomFeatures")
router.register('houses', apis.HouseViewSet, "houses")
router.register('roomRequests', apis.RoomRequestViewSet, "roomRequests")
router.register('favorites', apis.FavoriteViewSet, "favorites")
router.register('categories', apis.CategoryViewSet, "categories")
router.register('rentalData', apis.RentalDataViewSet, 'rentalData')
router.register('rewards', apis.RewardViewSet, 'rewards')
router.register('rewardTrackers', apis.RewardTrackerViewSet, 'rewardTrackers')
router.register('signup', apis.SignupUserViewSet, 'signup')
router.register('updatePassword', apis.UpdatePassword, 'updatePassword')
router.register('updateUser', apis.UpdateUser, 'updateUser')
router.register('deleteUser', apis.DeleteUser, 'deleteUser')
router.register('users', apis.UsersViewset, 'users')

urlpatterns = router.urls

