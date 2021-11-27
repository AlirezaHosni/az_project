from django.core.mail import message
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from chat.models import Chat_User
from login.models import Rate, Email_Verification, User



class IsAdvisor(permissions.BasePermission):
    message = "دعوت فقط از طرف مشاور انجام می‌شود"
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        return request.user.is_advisor


class IsChatExist(permissions.BasePermission):
    message = "چتی با مشخصات ارسال شده ثبت نشده است"

    def has_permission(self, request, view):
        try:
            chat_user = Chat_User.objects.filter(user=request.user.id, chat=view.kwargs['id']).first()
        except(Chat_User.DoesNotExist):
            return False

        
        return True


class IsChatDone(permissions.BasePermission):
    message = "چت هنوز به اتمام نرسیده است"

    def has_permission(self, request, view):
        try:
            chat_user = Chat_User.objects.filter(user=request.user.id, chat=view.kwargs['id']).first()
            if(chat_user.is_done == False):
                return False
        except(Chat_User.DoesNotExist):
            return False

        return True


class IsNotConfirmed(permissions.BasePermission):
    message="این نظر قبلا تایید شده است و امکان ویرایش نیست"
    def has_permission(self, request, view):
        try:
            rate = Rate.objects.filter(id=view.kwargs['id']).first()
            if(rate.is_confirmed == True):
                return False
        except(Rate.DoesNotExist):
            return False
        return True


class CanBeActive(permissions.BasePermission):
    message = "ابتدا در سایت ثبت نام کنید و سپس نسبت به فعالسازی اقدام نمایید"
    def has_permission(self, request, view):
        key = Email_Verification.objects.get(user_id=view.kwargs['user_id']).key
        token = view.kwargs['token']

        if key == token:
            return True

        return False