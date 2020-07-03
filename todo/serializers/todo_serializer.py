# -*- coding:utf-8 -*-
from rest_framework import serializers
from todo.models import Todo
from django.utils.dateparse import parse_datetime


class TodoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    priority = serializers.IntegerField()
    add_time = serializers.DateTimeField()

    class Meta:
        model = Todo
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(TodoSerializer, self).to_representation(instance)
        ret['add_time'] = instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        return ret

