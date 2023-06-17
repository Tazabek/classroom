from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cources.api.views import (CourcesAPIView, JoinCourceAPIView, 
                                    StreamAPIView, CourceUsersAPIView,
                                    CommentStreamAPIView, AddUserAPIView)

router = DefaultRouter()

router.register('cources', CourcesAPIView, basename='cources')
router.register('joincource', JoinCourceAPIView, basename='joincource')


urlpatterns = [
    path('courcestream/<int:pk>/', StreamAPIView.as_view(), name='courcestream'),
    path('courceusers/<int:pk>/', CourceUsersAPIView.as_view(), name='courceusers'),
    path('commentmessage/<int:pk>/', CommentStreamAPIView.as_view(), name='commentmessage'),
    path('adduser/<int:pk>/', AddUserAPIView.as_view(), name='adduser'),
    path('', include(router.urls))
]

