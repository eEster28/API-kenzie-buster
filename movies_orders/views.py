from rest_framework.views import APIView, Request, Response, status
from movies.models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from movies_orders.serializers import MovieOrdensSerializer


class MovieOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int):
        found_movie = get_object_or_404(Movie.objects.all(), id=movie_id)
        
        serializer = MovieOrdensSerializer(data=request.data)
    
        serializer.is_valid(raise_exception=True)
        
        serializer.save(user=request.user, movie=found_movie)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    
