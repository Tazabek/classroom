from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.cources.models import Cources, CourceStream, StreamComments
from django.db.models import Q


User = get_user_model()


class CourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cources
        fields = '__all__'
        read_only_fields = ['is_archived', 'teachers', 'students', 'code', 'owner']

    def create(self, validated_data):
        name = validated_data['name']
        subject = validated_data['subject']
        user = self.context['request'].user
        if Cources.objects.filter(Q(name=name) & Q(subject=subject)).exists():
            raise serializers.ValidationError(f'cource {name} already exists!')
        cource = Cources(
            name = name,
            subject = subject,
            owner = user
        )
        cource.save()
        cource.teachers.add(user)
        return cource
    
class UpdateCourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cources
        fields = '__all__'
        read_only_fields = ['code']
    

class JoinCourceSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=7, write_only=True)

    class Meta:
        model = Cources
        fields = '__all__'
        read_only_fields = ['name', 'subject', 'is_archived', 'teachers', 'students', 'code']

    def create(self, validated_data):
        code = validated_data['code']
        user = self.context['request'].user
        try:
            cource = Cources.objects.get(code=code)
            cource.students.add(user)
            return cource
        except Exception:
            raise serializers.ValidationError('Cource not found!')
    

class StreamCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamComments
        fields = '__all__'


class CourceStreamSerializer(serializers.ModelSerializer):
    comments = StreamCommentSerializer(many=True, allow_null=True)
    class Meta:
        model = CourceStream
        fields = ['id','text', 'date', 'is_group_message', 'comments']


class StreamSerialiser(serializers.ModelSerializer):
    stream = CourceStreamSerializer(many=True, allow_null=True, read_only=True)
    group_message = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Cources
        fields = ['stream', 'group_message']

    def create(self, validated_data):
        cource = self.context['view'].get_object()
        message = CourceStream(
            text = validated_data['group_message'],
            is_group_message = True,
            cource = cource
        )
        message.save()
        return message

    
class CommentGroupMessageSerializer(serializers.ModelSerializer):
    comments = StreamCommentSerializer(many=True, allow_null=True, read_only=True)
    text = serializers.CharField()

    class Meta:
        model = CourceStream
        fields = ['text', 'date', 'comments']

    def create(self, validated_data):
        stream = self.context['view'].get_object()
        user = self.context['request'].user
        if stream.is_group_message:
            comment = StreamComments(
                text = validated_data['text'],
                stream = stream,
                user = user
            )
            comment.save()
            return comment
        raise serializers.ValidationError('You can comment only group messages!')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image', 'is_owner']

class CourceUsersSerializer(serializers.ModelSerializer):
    teachers = UsersSerializer(many=True, allow_null=True, read_only=True)
    students = UsersSerializer(many=True, allow_null=True, read_only=True)
    class Meta:
        model = Cources
        fields = ['teachers', 'students']


class AddCourceUsersSerializer(serializers.ModelSerializer):
    teachers = UsersSerializer(many=True, allow_null=True, read_only=True)
    students = UsersSerializer(many=True, allow_null=True, read_only=True)
    add_teacher = serializers.EmailField(allow_null=True, write_only=True)
    add_student = serializers.EmailField(allow_null=True, write_only=True)
    class Meta:
        model = Cources
        fields = ['teachers', 'students', 'add_teacher', 'add_student'] 

    def create(self, validated_data):
        student = validated_data['add_student']
        teacher = validated_data['add_teacher']
        cource = self.context['view'].get_object()
        if student and teacher:
            raise serializers.ValidationError('You can not add a student and a teacher at the same time!')
        
        if student and User.objects.filter(email=student).exists():
                if cource.students.filter(email=student).exists() or cource.teachers.filter(email=student).exists():
                    raise serializers.ValidationError(f'User is already a member of the cource {cource.name}')
                student = User.objects.get(email=student)
                cource.students.add(student)
                return Response({'message': 'Student added successfully'}, status=201)
            
        if teacher and User.objects.filter(email=teacher).exists():
                if cource.teachers.filter(email=teacher).exists() or cource.students.filter(email=teacher).exists():
                    raise serializers.ValidationError(f'User is already a member of the cource {cource.name}')
                teacher = User.objects.get(email=teacher)
                cource.teachers.add(teacher)
                return Response({'message': 'Teacher added successfully'}, status=status.HTTP_201_CREATED)
        
        raise serializers.ValidationError('User is not registered')

