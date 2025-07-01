from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import (
    generics,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Donation
from core.permissions import IsDonor, IsReceiver
from core.serializers import (
    DonationSerializer,
    RegisterSerializer,
    UserDetailSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from datetime import datetime, timedelta

        from django.db.models import Count, Q

        # Basic stats
        total_users = User.objects.count()
        total_donations = Donation.objects.count()
        claimed_donations = Donation.objects.filter(
            is_claimed=True
        ).count()
        available_donations = Donation.objects.filter(
            is_claimed=False
        ).count()

        # User stats
        donor_users = User.objects.filter(
            profile__role="donor"
        ).count()
        receiver_users = User.objects.filter(
            profile__role="receiver"
        ).count()

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_donations = Donation.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        recent_claims = Donation.objects.filter(
            is_claimed=True, created_at__gte=thirty_days_ago
        ).count()

        # Food type breakdown
        food_type_stats = (
            Donation.objects.values("food_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Monthly trends (last 6 months)
        monthly_stats = []
        for i in range(6):
            month_start = datetime.now() - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            month_donations = Donation.objects.filter(
                created_at__gte=month_start, created_at__lt=month_end
            ).count()
            month_claims = Donation.objects.filter(
                is_claimed=True,
                created_at__gte=month_start,
                created_at__lt=month_end,
            ).count()
            monthly_stats.append(
                {
                    "month": month_start.strftime("%B %Y"),
                    "donations": month_donations,
                    "claims": month_claims,
                }
            )

        # Recent donations for admin review
        recent_donations_list = Donation.objects.select_related(
            "donor", "claimed_by"
        ).order_by("-created_at")[:10]

        return Response(
            {
                "total_users": total_users,
                "total_donations": total_donations,
                "claimed_donations": claimed_donations,
                "available_donations": available_donations,
                "donor_users": donor_users,
                "receiver_users": receiver_users,
                "recent_donations_30d": recent_donations,
                "recent_claims_30d": recent_claims,
                "food_type_stats": list(food_type_stats),
                "monthly_trends": monthly_stats,
                "recent_donations_list": DonationSerializer(
                    recent_donations_list, many=True
                ).data,
                "claim_rate": (
                    (claimed_donations / total_donations * 100)
                    if total_donations > 0
                    else 0
                ),
            }
        )


class AdminDonationsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Get all donations for admin management"""
        donations = Donation.objects.select_related(
            "donor", "claimed_by"
        ).order_by("-created_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

    def delete(self, request, donation_id):
        """Delete a donation (admin only)"""
        try:
            donation = Donation.objects.get(id=donation_id)
            donation.delete()
            return Response(
                {"message": "Donation deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Donation.DoesNotExist:
            return Response(
                {"error": "Donation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_permissions(self):
        # Admin users can do everything
        if self.request.user.is_superuser:
            return [permissions.IsAuthenticated()]

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

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def claimed_by_user(self, request):
        """Get all donations claimed by a specific user"""
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "user_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Only allow users to see their own claimed donations
        if int(user_id) != request.user.id:
            return Response(
                {
                    "error": "You can only view your own claimed donations"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        claimed_donations = Donation.objects.filter(
            claimed_by_id=user_id, is_claimed=True
        ).order_by("-created_at")

        serializer = DonationSerializer(claimed_donations, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def statistics(self, request):
        """Get donation statistics for map visualization"""
        try:
            # Get query parameters for filtering
            lat_min = request.query_params.get("lat_min", None)
            lat_max = request.query_params.get("lat_max", None)
            lng_min = request.query_params.get("lng_min", None)
            lng_max = request.query_params.get("lng_max", None)
            zoom_level = int(request.query_params.get("zoom", 10))

            # Base queryset
            queryset = Donation.objects.all()

            # Apply geographic bounds if provided
            if all([lat_min, lat_max, lng_min, lng_max]):
                queryset = queryset.filter(
                    latitude__gte=float(lat_min),
                    latitude__lte=float(lat_max),
                    longitude__gte=float(lng_min),
                    longitude__lte=float(lng_max),
                )

            # Get basic statistics
            total_donations = queryset.count()
            available_donations = queryset.filter(
                is_claimed=False
            ).count()
            claimed_donations = queryset.filter(
                is_claimed=True
            ).count()

            # Get food type breakdown
            food_type_stats = (
                queryset.values("food_type")
                .annotate(count=Count("id"))
                .order_by("-count")
            )

            # Get geographic clustering data
            if zoom_level >= 15:
                # High zoom: individual donations
                clusters = []
                for donation in queryset.filter(
                    latitude__isnull=False, longitude__isnull=False
                ):
                    clusters.append(
                        {
                            "center": [
                                donation.latitude,
                                donation.longitude,
                            ],
                            "donations": [donation.id],
                            "stats": {
                                "total": 1,
                                "available": (
                                    0 if donation.is_claimed else 1
                                ),
                                "claimed": (
                                    1 if donation.is_claimed else 0
                                ),
                                "food_types": {
                                    donation.food_type or "other": 1
                                },
                            },
                        }
                    )
            else:
                # Medium/low zoom: create clusters
                grid_size = 0.01 if zoom_level >= 10 else 0.05
                clusters = self._create_geographic_clusters(
                    queryset, grid_size
                )

            # Get recent activity
            recent_donations = queryset.order_by("-created_at")[:10]

            return Response(
                {
                    "summary": {
                        "total": total_donations,
                        "available": available_donations,
                        "claimed": claimed_donations,
                        "claim_rate": (
                            (
                                claimed_donations
                                / total_donations
                                * 100
                            )
                            if total_donations > 0
                            else 0
                        ),
                    },
                    "food_types": list(food_type_stats),
                    "clusters": clusters,
                    "recent_activity": DonationSerializer(
                        recent_donations, many=True
                    ).data,
                    "zoom_level": zoom_level,
                }
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to get statistics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _create_geographic_clusters(self, queryset, grid_size):
        """Create geographic clusters based on grid size"""
        clusters = {}

        for donation in queryset.filter(
            latitude__isnull=False, longitude__isnull=False
        ):
            # Create grid key
            grid_x = int(donation.latitude / grid_size)
            grid_y = int(donation.longitude / grid_size)
            key = f"{grid_x},{grid_y}"

            if key not in clusters:
                clusters[key] = {
                    "center": [0, 0],
                    "donations": [],
                    "bounds": [
                        [float("inf"), float("inf")],
                        [float("-inf"), float("-inf")],
                    ],
                    "stats": {
                        "total": 0,
                        "available": 0,
                        "claimed": 0,
                        "food_types": {},
                    },
                }

            cluster = clusters[key]
            cluster["donations"].append(donation.id)

            # Update bounds
            cluster["bounds"][0][0] = min(
                cluster["bounds"][0][0], donation.latitude
            )
            cluster["bounds"][0][1] = min(
                cluster["bounds"][0][1], donation.longitude
            )
            cluster["bounds"][1][0] = max(
                cluster["bounds"][1][0], donation.latitude
            )
            cluster["bounds"][1][1] = max(
                cluster["bounds"][1][1], donation.longitude
            )

            # Update stats
            cluster["stats"]["total"] += 1
            if donation.is_claimed:
                cluster["stats"]["claimed"] += 1
            else:
                cluster["stats"]["available"] += 1

            food_type = donation.food_type or "other"
            cluster["stats"]["food_types"][food_type] = (
                cluster["stats"]["food_types"].get(food_type, 0) + 1
            )

        # Calculate centers
        for cluster in clusters.values():
            if cluster["donations"]:
                # Get the actual donations to calculate center
                donations = queryset.filter(
                    id__in=cluster["donations"]
                )
                total_lat = sum(d.latitude for d in donations)
                total_lng = sum(d.longitude for d in donations)
                cluster["center"] = [
                    total_lat / len(donations),
                    total_lng / len(donations),
                ]

        return list(clusters.values())


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserDetailSerializer

    def get_queryset(self):
        # Users can only view their own profile or public profiles
        if self.action == "retrieve":
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        # Only allow users to update their own profile
        if int(kwargs.get("pk")) != request.user.id:
            return Response(
                {"error": "You can only update your own profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Only allow users to update their own profile
        if int(kwargs.get("pk")) != request.user.id:
            return Response(
                {"error": "You can only update your own profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def donations(self, request, pk=None):
        """Get all donations by a specific user"""
        user = self.get_object()
        donations = Donation.objects.filter(donor=user).order_by(
            "-created_at"
        )
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)


class UserDonationsView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Donation.objects.filter(donor_id=user_id).order_by(
            "-created_at"
        )
