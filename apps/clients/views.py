from functools import partial

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Client

from .serializers import (
    ClientArchiveSerializer,
    ClientListSerializer,
    ClientDetailSerializer,
    ClientCreateSerializer,
    ClientUpdateSerializer
)


class ClientListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.filter(agent_id=self.request.user.id)
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data,
                                            context = {'request': request})
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientDetailSerializer(client).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientListViewALL(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk, agent_id=self.request.user.id)
        except Client.DoesNotExist:
            return None

    def get(self, request, pk):
        client = self.get_object(pk)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def patch(self, request, pk):
        client = self.get_object(pk)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientUpdateSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientDetailSerializer(client).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class ClientArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientArchiveSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientDetailSerializer(client).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
