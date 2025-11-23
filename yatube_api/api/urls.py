from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path(r'posts/<int:post_id>/comments/',
         CommentViewSet.as_view({
             'get': 'list',
             'post': 'create',
         })),
    path(r'posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'update',
             'delete': 'destroy',
         })),


    # Auth urls
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
