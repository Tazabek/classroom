from rest_framework.permissions import BasePermission

class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.cource.teachers.all():
            return True
        return request.user in obj.cource.students.all()