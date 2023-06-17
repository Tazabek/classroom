from rest_framework import permissions
from rest_framework import mixins, viewsets, generics
from apps.cources.api.serializers import (CourceSerializer, JoinCourceSerializer, CourceUsersSerializer,
                                          StreamSerialiser, AddCourceUsersSerializer, UsersSerializer,
                                          UpdateCourceSerializer, CommentGroupMessageSerializer)
from apps.cources.api.permissions import IsOwner, IsTeacher, IsStudent, IsGroupMessage, IsStudentOrTeacher
from django.contrib.auth import get_user_model
from apps.cources.models import Cources, CourceStream
from django.db.models import Q

User = get_user_model()


class CourcesAPIView(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = Cources.objects.filter(Q(teachers=user) | Q(students=user))
        return queryset

    def get_serializer_class(self):
        if self.action in ['update']:
            return UpdateCourceSerializer
        return CourceSerializer

    permission_by_action = {
        'list': [IsStudentOrTeacher],
        'create': [permissions.IsAuthenticated],
        'retrieve': [IsStudentOrTeacher],
        'update': [IsOwner],
        'delete': [IsOwner],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class JoinCourceAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = JoinCourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cources.objects.filter(students=user)
        return queryset
    

class StreamAPIView(generics.RetrieveAPIView,
                    generics.ListCreateAPIView,
                    generics.ListAPIView):
    queryset = Cources.objects.all().prefetch_related('stream')
    serializer_class = StreamSerialiser
    permission_classes = [IsStudentOrTeacher]

    

class CourceUsersAPIView(generics.RetrieveAPIView,
                         generics.ListAPIView):
    queryset = Cources.objects.all().prefetch_related('teachers', 'students')
    serializer_class = CourceUsersSerializer
    permission_classes = [IsStudentOrTeacher]


class AddUserAPIView(generics.RetrieveAPIView,
                     generics.ListCreateAPIView):
    queryset = Cources.objects.all().prefetch_related('teachers', 'students')
    serializer_class = AddCourceUsersSerializer
    permission_classes = [IsTeacher]


class CommentStreamAPIView(generics.RetrieveAPIView,
                           generics.ListCreateAPIView,
                           generics.ListAPIView):
    queryset = CourceStream.objects.all().prefetch_related('comments')
    serializer_class = CommentGroupMessageSerializer
    permission_classes = [IsGroupMessage]