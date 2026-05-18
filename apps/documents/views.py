from functools import partial
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..policies.models import Policy
from .models import Document
from .serializers import (
    DocumentListSerializer,
    DocumentDetailDeleteSerializer,
    DocumentUploadSerializer
)


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        
        policies = Policy.objects.filter(agent_id=request.user)
        documents = Document.objects.filter(policy_id__in=policies)
        
        serializer = DocumentListSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            document = serializer.save()
            return Response(DocumentDetailDeleteSerializer(document).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            document = Document.objects.get(id=pk)
        except Document.DoesNotExist:
            return Response({'detail': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DocumentDetailDeleteSerializer(document)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            document = Document.objects.get(id=pk)
        except Document.DoesNotExist:
            return Response({'detail': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentDetailDeleteSerializer(document)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    