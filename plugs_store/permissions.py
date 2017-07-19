from rest_framework import permissions


class StaffOrReadOnly(permissions.BasePermission):
    """
    Object level permission to restrict users that are not accountants
    from updating members data
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated() and request.user.is_staff


class AdminOrReadOnly(permissions.BasePermission):
    """
    Object level permission to restrict users that are not accountants
    from updating members data
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated() and request.user.is_superuser
