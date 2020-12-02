from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_by = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.title}'


class Album(models.Model):
    album_name = models.CharField(max_length=30)
    album_date = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(User,on_delete=models.CASCADE,related_name='albums')

    def __str__(self):
        return f'{self.album_name}'


class Tracks(models.Model):
    track_name = models.CharField(max_length=20)
    track_duration = models.DurationField()
    album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name='tracks')

    def __str__(self):
        return f'{self.track_name}'