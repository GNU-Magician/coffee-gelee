from django.db import models
import os
from django.contrib.auth.models import User
import datetime
# Create your models here.
from django.conf import settings

class Post(models.Model):
    name = models.CharField(max_length=200, help_text='Post name')
    file = models.FileField(upload_to='{}/{:%Y/%B/%d}'.format(settings.MEDIA_ROOT, datetime.datetime.now()), blank=True)

    post_date = models.DateTimeField()
    description = models.TextField(max_length=3000, help_text="Post description")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    can_view = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def filename(self):
        return os.path.basename(self.file.name)

    def xd(self):
        return "detail/" + "media/" + str(self.relative())

    class Meta:
        permissions = (('can_delete_posts', 'can_view_posts'),)


class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Category name:")
    parent_name = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=1000, help_text="Category description.", null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, help_text="Tag name: ")

    def __str__(self):
        return self.name

