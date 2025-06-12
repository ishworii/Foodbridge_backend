from django.contrib.auth.models import User
from django.db import models


class Donation(models.Model):
    donor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="donations"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
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
