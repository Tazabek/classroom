from django.shortcuts import render
from django.contrib.auth import get_user_model
from apps.users.api.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework import permissions

User = get_user_model()


class UserAPIView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_by_action = {
        'list': [permissions.IsAdminUser],
        'create': [permissions.AllowAny],
        'retrieve': [permissions.IsAdminUser],
        'delete': [permissions.IsAdminUser],
    }
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
