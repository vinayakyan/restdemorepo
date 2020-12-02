from rest_framework import serializers
from .models import Post,Tracks,Album
from django.contrib.auth.models import User


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=20)
    content = serializers.CharField(max_length=100)
    created_by = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.created_by = validated_data.get('created_by')
        instance.save()
        return instance


class PostModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id','title','content','created_by']


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracks
        fields = ['id','track_name','track_duration']


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id','album_name','album_date','tracks']


class UserSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['id','username','password','email','is_active','albums']

    def create(self, validated_data):
        album_data = validated_data.pop('albums')
        user = User.objects.create(**validated_data)
        for album in album_data:
            tracks = album.pop('tracks')
            print(album,tracks)
            new_album = Album.objects.create(artist=user,**album)
            for track in tracks:
                t = Tracks.objects.create(album = new_album,**track)
        return user

