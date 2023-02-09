from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        created = self.created.strftime('%d/%m/%Y, %H:%M:%S')
        return self.title + ' - User: ' + self.user.username + ' - Created: ' + str(created)

