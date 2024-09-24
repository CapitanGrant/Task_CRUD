from django.urls import path
from .views import TaskRegistration, TaskList, TaskDetail, TaskDelete, TaskDeleteAll, TaskUpdate

urlpatterns = [
    path('register/', TaskRegistration.as_view(), name='task-register'),
    path('task/<int:task_id>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('delete/<int:task_id>/', TaskDelete.as_view(), name='task-delete'),
    path('delete-all/', TaskDeleteAll.as_view(), name='task-delete-all'),
    path('update/<int:task_id>/', TaskUpdate.as_view(), name='task-update'),
]
