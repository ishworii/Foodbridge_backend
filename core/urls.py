from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (
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
