from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer,PostModelSerializer,TrackSerializer,AlbumSerializer,UserSerializer
from .models import Post,Tracks,Album
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def first_api(request):
    return Response({'message': 'this is demo message for rest api'})


class SecondApi(APIView):
    #authentication_classes = [BasicAuthentication,SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        print(request.query_params)
        f = request.query_params.get('xyz')
        z = request.query_params.get('pqr')
        print(f,z)
        return Response({'message': 'this is second api'})

    def post(self, request, *args, **kwargs):
        print(request.data,request.query_params)
        return Response({'message': 'this is second api'})


@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle])
def post_api(request):
    if request.method == 'POST':
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post.save()
            return Response(post.data)
        return Response(post.errors)
    all_posts = Post.objects.all()
    serializer = PostSerializer(all_posts, many=True)
    return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
@throttle_classes([AnonRateThrottle])
def post_api_RUD(request,pk):
    try:
        obj = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'message': 'Bad Request'})
    if request.method == 'GET':
        serializer = PostSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        obj.delete()
        return Response({'message': 'No Record to Display'})


class PostAPI(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


class PostAPIRUD(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


class PostViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            queryset = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'message': 'Bad Request'})
        serializer = PostModelSerializer(queryset)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            queryset = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'message': 'Bad Request'})
        serializer = PostModelSerializer(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            queryset = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'message': 'Bad Request'})
        queryset.delete()
        return Response({'message': 'No Record To Display'})

    def create(self, request, *args, **kwargs):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class PostModelViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


class UserAPIView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AlbumApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

