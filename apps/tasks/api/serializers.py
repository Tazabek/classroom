from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import empty
from apps.cources.models import Cources, CourceStream
from apps.tasks.models import (Themes, Tasks, Comments, Points)


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Themes
        fields = ['name']


class AddTaskSerializer(serializers.ModelSerializer):
    theme = serializers.PrimaryKeyRelatedField(queryset=Themes.objects.all(), allow_null=True, required=False)
    new_theme = serializers.CharField(max_length=155, write_only=True, allow_null=True)

    class Meta:
        model = Tasks
        fields = ['id', 'name', 'instruction', 'file', 'points', 'added_at', 'deadline', 'theme', 'new_theme', 'cource']

    def create(self, validated_data):
        cource = self.context['view'].get_object()
        new_theme = validated_data['new_theme']
        user = self.context['request'].user

        if new_theme and not Themes.objects.filter(name=new_theme).exists():
            theme = Themes(name=new_theme,
                           cource=cource)
            theme.save()
            task = Tasks(
                name = validated_data['name'],
                instruction = validated_data['instruction'],
                file = validated_data['file'],
                points = validated_data['points'],
                deadline = validated_data['deadline'],
                theme = theme,
                cource = cource
            )
            task.save()
            stream = CourceStream(
                message = f'{user.username} added a task {task.name}',
                cource = cource
            )
            stream.save()
            return task
        else:
            task = Tasks(
                name = validated_data['name'],
                instruction = validated_data['instruction'],
                file = validated_data['file'],
                points = validated_data['points'],
                deadline = validated_data['deadline'],
                cource = cource
            )
            task.save()
            stream = CourceStream(
                message = f'{user.username} added a task {task.name}',
                cource = cource
            )
            stream.save()
            return task



class TasksSerializer(serializers.ModelSerializer):
    task = AddTaskSerializer(many=True, allow_null=True, read_only=True)
    theme = ThemeSerializer(many=True, allow_null=True)

    class Meta:
        model = Cources
        fields = ['theme', 'task']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class CommentTaskSerializer(serializers.ModelSerializer):
    comment = CommentsSerializer(many=True, allow_null=True, read_only=True)
    text = serializers.CharField(write_only=True)

    class Meta:
        model = Tasks
        fields = ['name', 'comment', 'text']
        read_only_fields = ['name']

    def create(self, validated_data):
        task = self.context['view'].get_object()
        user = self.context['request'].user
        comment = Comments(
            text = validated_data['text'],
            task = task,
            user = user
            )
        comment.save()
        return comment
    

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        fields = ['points', 'student']


class TaskPointsSerializer(serializers.ModelSerializer):
    point = PointsSerializer(many=True, allow_null=True, read_only=True)

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)

        if instance is not None:
            self.field_name = instance
            self.fields[self.field_name] = serializers.CharField()

    class Meta:
        model = Tasks
        fields = ['name', 'point']



        


