from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


class Donation(models.Model):
    donor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="donations"
    )
    title = models.CharField(max_length=100)
    description = RichTextField()
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    food_type = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to="donations/", null=True, blank=True
    )
    is_claimed = models.BooleanField(default=False)
    claimed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claims",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    ROLE_CHOICES = (
        ("donor", "Donor"),
        ("receiver", "Receiver"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
