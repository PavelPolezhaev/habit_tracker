from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """Проверяет является ли пользователь владельцом"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
