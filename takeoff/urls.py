from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from takeoffapi.views import UserView, TripView, LodgingView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')
router.register(r'trip', TripView, 'trip')
router.register(r'lodging', LodgingView, 'lodging')


urlpatterns = [
    path('', include(router.urls))
]
