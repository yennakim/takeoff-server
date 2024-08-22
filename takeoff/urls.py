from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from takeoffapi.views import UserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')

urlpatterns = [
    path('', include(router.urls))
]
