from rest_framework.views import APIView, Request, Response, status
from movies.models import Movie
from movies.serializers import MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsAdminOrReadOnly 
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    
    def get(self, request: Request):
        movies = Movie.objects.all()
        
        result_page = self.paginate_queryset(movies, request, view=self)
        
        serializer = MovieSerializer(result_page, many=True)
        
        return self.get_paginated_response(serializer.data)
    

class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT) 



