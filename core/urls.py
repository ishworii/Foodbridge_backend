from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (
    AdminDonationsView,
    AdminStatsView,
    DonationViewSet,
    MeView,
    RegisterView,
    UserDonationsView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"donations", DonationViewSet, basename="donation")
router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "admin/stats/", AdminStatsView.as_view(), name="admin-stats"
    ),
    path(
        "admin/donations/",
        AdminDonationsView.as_view(),
        name="admin-donations",
    ),
]


urlpatterns += [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path(
        "users/<int:user_id>/donations/",
        UserDonationsView.as_view(),
        name="user-donations",
    ),
]
