from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from .models import Message, Chat_User
from django.utils import timezone


class IsAdvisor(permissions.BasePermission):
    message = "وضعیت چت فقط توسط مشاور تغییر خواهد کرد"
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        return request.user.is_advisor

class IsChatGetStarted(permissions.BasePermission):
    message= "امکان ارسال پیام وجود ندارد"
    def has_permission(self, request, view):
        try:
            chat_user = Chat_User.objects.filter(user=request.user.id, chat=view.kwargs['id']).first()
        except(Chat_User.DoesNotExist):
            return False
        
        if timezone.now() < chat_user.chat_start_datetime:
            return False
        return True

class IsChatDone(permissions.BasePermission):
    message = "چت به اتمام رسیده است"

    def has_permission(self, request, view):
        try:
            chat_user = Chat_User.objects.filter(user=request.user.id, chat=view.kwargs['id']).first()
            if(chat_user.is_done == True):
                return False
        except(Chat_User.DoesNotExist):
            return False

        return True




