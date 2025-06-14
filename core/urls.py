from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DonationViewSet, RegisterView

router = DefaultRouter()
router.register(r"donations", DonationViewSet, basename="donation")


urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += [
    path("register/", RegisterView.as_view(), name="register"),
    
]
