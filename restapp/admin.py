from django.contrib import admin
from .models import Post,Album,Tracks
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','content','created_by']


admin.site.register(Post,PostAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id','album_name','album_date','artist']


admin.site.register(Album,AlbumAdmin)


class TracksAdmin(admin.ModelAdmin):
    list_display = ['id', 'track_name', 'track_duration', 'album']


admin.site.register(Tracks,TracksAdmin)