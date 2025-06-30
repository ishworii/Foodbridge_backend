from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Donation, Profile


class DonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(
        source="donor.username", read_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = "__all__"
        read_only_fields = ["id", "donor", "created_at"]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)
        user.profile.role = role
        user.profile.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role")

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = fields


class UserDetailSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role")
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S"
    )
    last_login = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S", allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "date_joined",
            "last_login",
        ]
        read_only_fields = fields


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
        read_only_fields = ["id"]
