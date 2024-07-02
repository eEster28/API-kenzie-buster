from rest_framework import serializers
from movies_orders.models import MovieOrder


class MovieOrdensSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True, source="movie.title")
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    purchased_by = serializers.CharField(read_only=True, source="user.email")
    purchased_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)
    

