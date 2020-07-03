from django.shortcuts import render
from .models import Todo
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

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
    try:
        todos = Todo.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", todos))
        response['msg'] = "success"
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
