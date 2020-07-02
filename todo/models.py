from django.db import models


# Create your models here.
class Todo(models.Model):
    priority = models.IntegerField("priority of task")
    name = models.TextField()
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
