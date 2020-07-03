import json
from .models import Todo
from django.views.decorators.http import require_http_methods
from .serializers.todo_serializer import TodoSerializer
from django.http import JsonResponse

# Create your views here.
@require_http_methods(['GET'])
def add_todo(request):
    response = {}
    try:
        todo = Todo(name=request.GET.get('name'), priority=request.GET.get('priority'))
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
        todos = Todo.objects.all()
        for ele in todos:
            print('ele is ', ele)
            data = TodoSerializer(ele).data
            print('xxx data is ', data)
            print('data.data is ', data)
            data_list.append(data)
        response['list'] = data_list
        response['msg'] = "success"
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
