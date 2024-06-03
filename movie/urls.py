from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import ActorViewSet, MovieViewSet, MovieActorAPIView,CommentViewSet,UserCommentsView,DeleteCommentView

# ResAPIView,

router = routers.DefaultRouter()
router.register('actor', ActorViewSet)
router.register('movie', MovieViewSet)
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    # path('kino/',ResAPIView.as_view(), name='kino')
    # path('movies/',MovieAPIView.as_view(),name='movies'),
    # path('actors/',ActorAPIView.as_view(),name='actors'),
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('movies/<int:id>/actors/', MovieActorAPIView.as_view(), name='movie-actor-list'),
    path('user-comments/', UserCommentsView.as_view(), name='user-comments'),
    path('delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete-comment'),

]
