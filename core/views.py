from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Donation
from core.permissions import IsDonor, IsReceiver
from core.serializers import DonationSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def get_permissions(self):
        # Only donors can create, update or delete donations
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [permissions.IsAuthenticated(), IsDonor()]
        # Only receivers can claim donations
        if self.action == "claim":
            return [permissions.IsAuthenticated(), IsReceiver()]
        # Authenticated users can list and retrieve
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Automatically set the donor to the logged-in user
        serializer.save(donor=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, IsReceiver],
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

        return Response(
            {"success": "Donation claimed successfully."},
            status=status.HTTP_200_OK,
        )
