from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Donation
from .serializers import DonationSerializer, RegisterSerializer


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def claim(self, request, pk=None):
        donation = self.get_object()

        if donation.is_claimed:
            return Response(
                {"error": "This donation has already been claimed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        donation.is_claimed = True
        donation.claimed_by = request.user
        donation.save()

        return Response({"success": "Donation claimed successfully."})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
