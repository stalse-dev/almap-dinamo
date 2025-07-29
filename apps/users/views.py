from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions, DjangoModelPermissions
from rest_framework import status, viewsets
from apps.users.models import CustomUser
from apps.users.serializers import CustomUserSerializer, GroupSerializer

# Create your views here.

class WhoAmIView(APIView):
    """
    View to return the authenticated user's information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CustomUser instances.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]    


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing groups.
    """
    # Assuming you have a Group model and serializer
    queryset = Group.objects.all()  # Replace with actual Group model
    serializer_class = GroupSerializer  # Replace with actual Group serializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]