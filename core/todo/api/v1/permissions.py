from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsTaskOwner(BasePermission):
    message = "No permission to view this task."

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            raise PermissionDenied(detail=self.message)
