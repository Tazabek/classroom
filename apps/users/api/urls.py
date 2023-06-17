from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.api.views import UserAPIView
from apps.cources.api.urls import CourcesAPIView

router = DefaultRouter()


router.register('api/v1/users', UserAPIView, basename='users')


urlpatterns = [
    path('', include(router.urls))
]

