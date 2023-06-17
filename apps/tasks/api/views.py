from rest_framework import mixins, viewsets, generics, permissions
from apps.cources.models import Cources
from apps.tasks.models import (Tasks, Themes, Comments)
from apps.tasks.api.serializers import (TasksSerializer, AddTaskSerializer,
                                        TaskPointsSerializer, CommentTaskSerializer)
from apps.tasks.api.permission import IsMember
from apps.cources.api.permissions import IsTeacher, IsStudent, IsStudentOrTeacher

class TasksAPIView(generics.RetrieveAPIView,
                     generics.ListAPIView):
    queryset = Cources.objects.all().prefetch_related('theme', 'task')
    serializer_class = TasksSerializer
    permission_classes = [IsStudentOrTeacher]


class AddTaskAPIView(generics.RetrieveAPIView,
                     generics.ListCreateAPIView):
    queryset = Cources.objects.all().prefetch_related('theme', 'task')
    serializer_class = AddTaskSerializer
    permission_classes = [IsTeacher]


class CommentTaskAPIView(generics.RetrieveAPIView,
                        generics.ListCreateAPIView,
                        generics.ListAPIView):
    queryset = Tasks.objects.all().prefetch_related('comment')
    serializer_class = CommentTaskSerializer
    permission_classes = [IsMember]


class PointsAPIView(generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.ListCreateAPIView):
    queryset = Tasks.objects.all().prefetch_related('point')
    serializer_class = TaskPointsSerializer