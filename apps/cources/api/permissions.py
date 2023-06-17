from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = obj.owner
        return bool(owner == request.user)
    
class IsTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        teachers = obj.teachers.all()
        return bool(user in teachers)
    
class IsStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        students = obj.students.all()
        return bool(user in students)
    

class IsGroupMessage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.is_group_message == True)
    

class IsStudentOrTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        students = obj.students.all()
        teachers = obj.teachers.all()
        return bool(user in teachers or user in students)