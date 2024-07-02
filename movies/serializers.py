from rest_framework import serializers
from movies.models import Movie, BookRating

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration =  serializers.CharField(max_length=20, allow_blank=True, default="")
    rating = serializers.ChoiceField(choices=BookRating.choices, default=BookRating.G)
    synopsis = serializers.CharField(allow_blank=True, default="")
    
    added_by = serializers.CharField(read_only=True, source="user.email")
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
   
    

