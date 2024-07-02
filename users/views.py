from rest_framework.views import APIView, Response, Request, status
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUserOwner

class UserView(APIView):

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner]
 
   
    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User.objects.all(), id=user_id)
        
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)
    
    
    def patch(self, request: Request, user_id: int):
        found_user = get_object_or_404(User, id=user_id)
        
        self.check_object_permissions(request, found_user)
        
        serializer = UserSerializer(found_user, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status.HTTP_200_OK)
    