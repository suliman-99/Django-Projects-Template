from rest_framework import permissions


def IsOwnerOrReadOnlyBuilder(field_name: str):
    class IsOwnerOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            
            parts = field_name.split('.')
            temp_obj = obj
            for part in parts:
                temp_obj = getattr(temp_obj, part)
            return bool(temp_obj == request.user)
    return IsOwnerOrReadOnly
