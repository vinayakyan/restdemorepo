from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import first_api,SecondApi,post_api,post_api_RUD,PostAPI,PostAPIRUD,PostModelViewSet,UserAPIView,AlbumApiView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
route = DefaultRouter()
route.register('mpost',PostModelViewSet)
router = DefaultRouter()
router.register('user',UserAPIView)

urlpatterns =[
    path('first/', first_api, name='first-api'),
    path('second/', SecondApi.as_view(), name='second-api'),
    path('post/', post_api, name='post-api'),
    path('post/<int:pk>/',post_api_RUD,name='post-api-RUD'),
    path('cpost/',PostAPI.as_view(),name='PostAPI'),
    path('cpost/<int:pk>/',PostAPIRUD.as_view(),name='PostAPIRUD'),
    path('',include(route.urls)),
    path('',include(router.urls)),
    path('album/<int:pk>/',AlbumApiView.as_view(),name='albumrud'),
    path('api/token/',TokenObtainPairView.as_view(),name='token-obtain-pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token-refresh'),
]