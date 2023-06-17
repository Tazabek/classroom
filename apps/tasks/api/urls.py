from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.api.views import TasksAPIView, PointsAPIView, CommentTaskAPIView

router = DefaultRouter()

urlpatterns = [
    path('tasks/<int:pk>/', TasksAPIView.as_view(), name='addtask'),
    path('commenttask/<int:pk>/', CommentTaskAPIView.as_view(), name='commenttask'),
    path('points/<int:pk>/', PointsAPIView.as_view(), name='points'),
    path('', include(router.urls)),
]
