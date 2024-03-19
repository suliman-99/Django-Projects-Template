from collections.abc import Iterable
from rest_framework import permissions


class ModelPermissions(permissions.BasePermission):
    action_map = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }
    
    def has_permission(self, request, view):
        perms = []
        models = getattr(view, 'permission_models', None)

        if not models:
            models = []

        if not isinstance(models, Iterable):
            models = (models, )

        for model in models:
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            action = ModelPermissions.action_map[request.method]
            perms.append(f'{app_label}.{action}_{model_name}')

        return request.user.has_perms(perms)


class MethodBasedRequiredPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        perms = getattr(view, 'permission_required', None)

        if isinstance(perms, dict):
            perms = perms.get(request.method, [])

        if isinstance(perms, str):
            perms = (perms, )

        if perms is None:
            perms = []

        return request.user.has_perms(perms)


class ActionBasedRequiredPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        perms = getattr(view, 'permission_required', None)

        if isinstance(perms, dict):
            perms = perms.get(view.action, [])

        if isinstance(perms, str):
            perms = (perms, )

        if perms is None:
            perms = []

        return request.user.has_perms(perms)


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_superuser
        )


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )
