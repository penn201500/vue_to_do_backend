import json

from django.db.models import Q

from .models import Todo
from django.views.decorators.http import require_http_methods
from .serializers.todo_serializer import TodoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


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
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


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
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def search(request):
    response = {}
    data_list = []
    try:
        # search_txt = request.query_params.get('search')
        data = json.loads(request.body)
        search_txt = data.get('search_txt') if data else ''
        print(search_txt)
        if search_txt.isdigit():
            print('here')
            todos = Todo.objects.filter(is_del=False).filter(
                Q(id=int(search_txt)) | Q(priority=int(search_txt)) | Q(name__icontains=search_txt) | Q(
                    comment__icontains=search_txt) | Q(todo_type=int(search_txt)))
        else:
            todos = Todo.objects.filter(is_del=False).filter(
                Q(name__icontains=search_txt) | Q(comment__icontains=search_txt))
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
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
