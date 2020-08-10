import json
from .models import Todo
from django.views.decorators.http import require_http_methods
from .serializers.todo_serializer import TodoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
