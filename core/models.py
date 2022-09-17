from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField


class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = RichTextField()
    done = models.BooleanField(default=False)
    date = models.DateField(null=True)
    

