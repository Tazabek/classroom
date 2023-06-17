from django.urls import path, include
from apps.tasks.views import *

urlpatterns = [
    path('cource-tasks/<int:pk>/', cource_tasks, name='cource-tasks'),
    path('add-task/<int:pk>/', add_task, name='add-task'),
    path('task-detail/<int:pk>', task_detail, name='task-detail'),
    path('all-points/<int:pk>', all_points, name='all-points'),
    path('add-points/<int:pk>/', task_points, name='task-points'),
    path('update-point/<int:pk>/', update_points, name='update-point'),
    path('add-file/<int:pk>/', add_file, name='add-file'),
    path('update-file/<int:pk>/', change_file, name='change-file'),
    path('change-task/<int:pk>/', change_task, name='change-task'),
    path('api/v1/', include('apps.tasks.api.urls'))
]
