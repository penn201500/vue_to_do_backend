from django.db import models


# Create your models here.
class Todo(models.Model):
    TYPE_CHOICE = (
        (0, '生活'),
        (1, '工作'),
        (2, '充电'),
    )
    priority = models.IntegerField("priority of task")
    name = models.TextField()
    comment = models.TextField(default='')
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
    todo_type = models.IntegerField(choices=TYPE_CHOICE, default=0)
    is_del = models.BooleanField("删除标记", default=False)
