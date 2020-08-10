import json

import django_filters
from django.db.models import Q
from .models import Todo
from django.views.decorators.http import require_http_methods
from .serializers.todo_serializer import TodoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


# class TodoTypeFilter(django_filters.FilterSet):
#     todo_type = django_filters.CharFilter(method='filter_todo_type')
#
#     @staticmethod
#     def filter_todo_type(queryset, name, value):
#         # create a dictionary string -> integer
#         value_map = {v: k for k, v in Todo.TYPE_CHOICE.items()}
#         # get the integer value for the input string
#         value = value_map[value]
#         return queryset.filter(todo_type=value)

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def add_todo(request):
    response = {}
    try:
        data = json.loads(request.body)
        todo = Todo(name=data.get('name'), priority=data.get('priority'), todo_type=data.get('todo_type'))
        todo.save()
        response['msg'] = 'success'
        response['error_num'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(['GET'])
def show_todos(request):
    response = {}
    data_list = []
    try:
        todos = Todo.objects.filter(is_del=False)
        for ele in todos:
            data = TodoSerializer(ele).data
            data_list.append(data)
        response['list'] = data_list
        response['msg'] = "success"
        response['error_num'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@require_http_methods(['GET'])
def search(request):
    response = {}
    data_list = []
    try:
        search_txt = request.GET.get('search_txt')
        value_map = dict((v, k) for k, v in Todo.TYPE_CHOICE)
        value = [v for k, v in value_map.items() if search_txt in k]
        if search_txt.isdigit():
            todos = Todo.objects.filter(is_del=False).filter(
                Q(id=int(search_txt)) | Q(priority=int(search_txt)) | Q(name__icontains=search_txt) | Q(
                    comment__icontains=search_txt) | Q(todo_type__in=value))
        else:
            todos = Todo.objects.filter(is_del=False).filter(
                Q(name__icontains=search_txt) | Q(comment__icontains=search_txt) | Q(todo_type__in=value))
        for ele in todos:
            data = TodoSerializer(ele).data
            data_list.append(data)
        response['list'] = data_list
        response['msg'] = "success"
        response['error_num'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@require_http_methods(['DELETE'])
def del_todos(request):
    response = {}
    ids = json.loads(request.body).get('ids')
    print(ids)
    todos = Todo.objects.filter(id__in=ids)
    try:
        todos.update(is_del=True)
        response['msg'] = "delete success"
        response['error_num'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
