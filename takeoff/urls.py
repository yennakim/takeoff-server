from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from takeoffapi.views import UserView, TripView, LodgingView, PackedItemView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')
router.register(r'trip', TripView, 'trip')
router.register(r'lodging', LodgingView, 'lodging')
router.register(r'items', PackedItemView, 'packed_item')


urlpatterns = [
    path('', include(router.urls))
]
