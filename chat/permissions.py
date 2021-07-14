from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404


class IsAdvisor(permissions.BasePermission):
    message = "چت فقط توسط مشاور امکان ایجاد دارد"
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        return request.user.is_advisor


