from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from takeoffapi.views import UserView, TripView, LodgingView, PackedItemView, BoardingPassView, TravelerView, TripTravelerView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')
router.register(r'trip', TripView, 'trip')
router.register(r'lodging', LodgingView, 'lodging')
router.register(r'items', PackedItemView, 'packed_item')
router.register(r'boarding_pass', BoardingPassView, 'boarding_pass')
router.register(r'traveler', TravelerView, 'traveler')
router.register(r'trip_traveler', TripTravelerView, 'trip_traveler')


urlpatterns = [
    path('', include(router.urls))
]
