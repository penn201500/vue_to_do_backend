from django.db import models


# Create your models here.
class Todo(models.Model):
    priority = models.IntegerField("priority of task")
    name = models.TextField()
    comment = models.TextField(default='')
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
    is_del = models.BooleanField("删除标记", default=False)
