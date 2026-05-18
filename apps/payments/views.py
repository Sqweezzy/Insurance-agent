from functools import partial

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..policies.models import Policy
from .models import Payment
from .serializers import(
    PaymentListCreateSerializer,
    PaymentDetailUpdateSerializer
)


class PaymentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user
        policy = Policy.objects.filter(agent_id=agent)
        payments = Payment.objects.filter(policy_id__in=policy)
        
        serializer = PaymentListCreateSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaymentListCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentListCreateSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            payment = Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            return Response({'detail': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentDetailUpdateSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            return Response({'detail': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentDetailUpdateSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentDetailUpdateSerializer(payment).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)