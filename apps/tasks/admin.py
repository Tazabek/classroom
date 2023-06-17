from django.contrib import admin
from apps.tasks.models import Tasks, Themes, Comments, Points, Files

class TasksInline(admin.TabularInline):
    model = Tasks
    extra = 1

class ThemesAdmin(admin.ModelAdmin):
    list_display = ['name', 'cource']
    inlines = [TasksInline]


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1

class PointsInline(admin.TabularInline):
    model = Points
    extra = 1

class FileInline(admin.TabularInline):
    model = Files
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [CommentsInline, PointsInline, FileInline]


admin.site.register(Themes, ThemesAdmin)
admin.site.register(Tasks, TaskAdmin)
