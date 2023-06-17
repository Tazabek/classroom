from django.urls import path, include
from apps.cources.views import *

urlpatterns = [
    path('', all_cources, name='allcources'),
    path('is_teacher/', is_teacher, name='teacher'),
    path('student/', is_student, name='student'),
    path('add_cource/', add_cource, name='addcource'),
    path('join-cource/', join_cource, name='join-cource'),
    path('cource-stream/<int:pk>/', cource_stream, name='cource-stream'),
    path('stream-comment/', add_stream_comment, name='add-stream-comment'),
    path('users/<int:pk>/', users, name='users'),
    path('add-teacher/<int:pk>/', add_teacher, name='add-teacher'),
    path('add-student/<int:pk>/', add_student, name='add-student'),
    path('logout/', logout, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('delete-cource/<int:pk>/', delete_cource, name='delete-cource'),
    path('leave-cource/<int:pk>/', leave_cource, name='leave-cource'),
    path('private-room/<int:pk>/', private_room, name='private-room'),
    path('private-room-with0teacher/<int:pk>/', teacher_private, name='private-with-teacher'),
    path('coming-tasks/<int:pk>/', comming_tasks, name='comming-tasks'),
    path('api/v1/', include('apps.cources.api.urls')),
]
