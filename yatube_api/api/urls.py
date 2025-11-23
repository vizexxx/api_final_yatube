from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CommentViewSet,
                    GroupViewSet,
                    FollowViewSet,
                    PostViewSet,)


router = SimpleRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register('posts', PostViewSet, basename='posts')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
