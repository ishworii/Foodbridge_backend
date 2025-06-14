from rest_framework import permissions


class IsDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.profile.role == "donor"
        )


class IsReceiver(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.profile.role == "receiver"
        )
