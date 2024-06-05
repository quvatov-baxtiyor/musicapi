from rest_framework import viewsets, status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Actor, Movie, Comments
from .serializers import ActorSerializer, MovieSerializer, CommentSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','year','genre']
    ordering_fields = ['genre','imdb_rating','-imdb_rating']



    @action(detail=True, methods=['POST'])
    def add_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        if not actor_id:
            return Response({"error": "Actor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response({"error": "Actor not found."}, status=status.HTTP_404_NOT_FOUND)

        movie.actors.add(actor)
        movie.save()

        serializer = ActorSerializer(movie.actors.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'])
    def remove_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        if not actor_id:
            return Response({"error": "Actor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response({"error": "Actor not found."}, status=status.HTTP_404_NOT_FOUND)

        movie.actors.remove(actor)
        movie.save()

        serializer = ActorSerializer(movie.actors.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieActorAPIView(APIView):
    def get(self,request,id,format=None):
        actors = Movie.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

class UserCommentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comments.objects.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({'error': 'Comment not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
