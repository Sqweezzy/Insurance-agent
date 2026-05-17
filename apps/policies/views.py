from functools import partial

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import InsuranceType, Policy
from .serializers import (
    InsuranceTypeSerializer,
    PolicyListSerializer,
    PolicyDetailSerializer,
    PolicyCreateSerializer,
    PolicyUpdateSerializer
)


class InsuranceTypeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        insurance_types = InsuranceType.objects.all()
        serializer = InsuranceTypeSerializer(insurance_types, many=True)
        return Response(serializer.data)


class PolicyDetailUpdateView(APIView):
    permission_classes =  [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Policy.objects.get(pk=pk, agent_id=self.request.user)
        except Policy.DoesNotExist:
            return None
    
    def get(self, request, pk):
        policy = self.get_object(pk)
        if not policy:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PolicyDetailSerializer(policy)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        policy = self.get_object(pk)
        if not policy:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PolicyUpdateSerializer(policy, data=request.data, context = {'request': request}, partial=True)
        if serializer.is_valid():
            policy = serializer.save()
            return Response(PolicyDetailSerializer(policy).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        policies = Policy.objects.filter(agent_id=request.user)
        serializer = PolicyListSerializer(policies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PolicyCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            policy = serializer.save()
            return Response(PolicyDetailSerializer(policy).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    