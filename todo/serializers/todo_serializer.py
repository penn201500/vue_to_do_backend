# -*- coding:utf-8 -*-
from rest_framework import serializers
from todo.models import Todo
from django.utils.dateparse import parse_datetime


class TodoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    priority = serializers.IntegerField()
    todo_type = serializers.IntegerField()
    add_time = serializers.DateTimeField()

    class Meta:
        model = Todo
        exclude = ('is_del', 'comment')

    def to_representation(self, instance):
        ret = super(TodoSerializer, self).to_representation(instance)
        ret['add_time'] = instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        ret['todo_type'] = instance.get_todo_type_display()
        return ret

