from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import Task
from .serializers import TaskSerializer


class TaskRegistration(APIView):
    @extend_schema(summary="Регистрация задачи",
                   description="Создаёт новую задачу с необязательным описанием. ",
                   request=TaskSerializer,
                   responses={
                       201: OpenApiResponse(response=TaskSerializer, description="Задача успешно создана"),
                       400: OpenApiResponse(description="Ошибки валидации")
                   }
                   )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({"status": "Task created", "id": task.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskList(APIView):
    @extend_schema(
        summary="Получение информации обо всех задачах",
        description="Возвращает список всех зарегистрированных задач.",
        responses={
            200: OpenApiResponse(response=TaskSerializer(many=True), description="Список всех задач")
        }
    )
    def get(self, request):
        users = Task.objects.all()
        serializer = TaskSerializer(users, many=True)
        return Response(serializer.data)


class TaskDetail(APIView):
    @extend_schema(
        summary="Получение информации о задаче",
        description="Возвращает информацию о задаче по его ID.",
        responses={
            200: OpenApiResponse(response=TaskSerializer, description="Информация о задаче"),
            404: OpenApiResponse(description="Задача не найдена")
        }
    )
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class TaskDelete(APIView):
    @extend_schema(
        summary="Удаление задачи",
        description="Удаляет задачу по его ID. Если задача не найдена, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Задача успешно удалена"),
            404: OpenApiResponse(description="Задача не найдена"),
            400: OpenApiResponse(description="ID задачи не предоставлен")
        }
    )
    def delete(self, request, task_id):
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                return Response({"status": "Task deleted"}, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Task ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteAll(APIView):
    @extend_schema(
        summary="Удаление всех задач",
        description="Удаляет все задачи из базы данных.",
        responses={
            200: OpenApiResponse(description="Все задачи успешно удалены")
        }
    )
    def delete(self, request):
        Task.objects.all().delete()
        return Response({"status": "All tasks deleted"}, status=status.HTTP_200_OK)


class TaskUpdate(APIView):
    @extend_schema(summary="Обновление задачи",
                   description="Позволяет сменить статус задачи, а так же описание и имя.",
                   request=TaskSerializer,
                   responses={
                       200: OpenApiResponse(response=TaskSerializer, description="Задача успешно обновлена"),
                       400: OpenApiResponse(description="Ошибки валидации"),
                       404: OpenApiResponse(description="Задача не найдена")
                   }
                   )
    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({"status": "Task updated", "id": task.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
