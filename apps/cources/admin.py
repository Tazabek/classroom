from django.contrib import admin
from apps.cources.models import Cources, CourceStream, StreamComments, PrivateRoom, Messages


class StreamInline(admin.TabularInline):
    model = CourceStream
    extra = 1


class CourcesAdmin(admin.ModelAdmin):
    inlines = [StreamInline]
    list_display = ['id', 'name']


class SreamCommentsInline(admin.TabularInline):
    model = StreamComments
    extra = 1


class CourceStreamAdmin(admin.ModelAdmin):
    list_display = ['is_group_message', 'text']
    inlines = [SreamCommentsInline]


class MessagesInline(admin.TabularInline):
    model = Messages
    extra = 1

class PrivateRoomAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher']
    inlines = [MessagesInline]


admin.site.register(Cources, CourcesAdmin)
admin.site.register(CourceStream, CourceStreamAdmin)
admin.site.register(PrivateRoom, PrivateRoomAdmin)