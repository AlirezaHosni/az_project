from django.core.mail import message
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from chat.models import Chat_User
from login.models import Rate, Email_Verification, Reservation, User
from datetime import timedelta
from .serializer import ReservationSerializer



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


# class IsChatFinishedByAdvisor(permissions.BasePermission):
#     message = "در حال حاضر مشاور در حال مشاوره دادن هست.ابتدا آن جلسه باید به اتمام برسد"
#     def has_permission(self, request, view):
#         serialized_data = ReservationSerializer(data=request.data)
#         serialized_data.is_valid(raise_exception=True)
#         reservation_datetime = serialized_data.validated_data['reservation_datetime']
#         end_session_datetime = reservation_datetime + timedelta(minutes=serialized_data.validated_data['duration_min'])
#         advisor_user_id = serialized_data.validated_data['receiver']
#         #print(advisor_user_id)
#         record_count = Reservation.objects.raw("select id, COUNT(*) as num_row from login_reservation where (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s) OR (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s)",
#          [reservation_datetime, reservation_datetime, advisor_user_id, end_session_datetime, end_session_datetime, advisor_user_id])

#         for n in record_count:
#             if n.num_row > 0:
#                 return False

#         return True

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


class CanReserveDatetime(permissions.BasePermission):
    message = "این بازه زمانی قبلا رزرو شده است یا هم اکنون مشاور مشغول جلسه دیگری هست"
    def has_permission(self, request, view):
        serialized_data = ReservationSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        reservation_datetime = serialized_data.validated_data['reservation_datetime']
        end_session_datetime = reservation_datetime + timedelta(minutes=serialized_data.validated_data['duration_min'])
        advisor_user_id = serialized_data.validated_data['receiver']
        #print(advisor_user_id)
        record_count = Reservation.objects.raw("select id, is_done from chat_chat_user where user_id in (select user_id from login_reservation where (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s) OR (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s))",
         [reservation_datetime, reservation_datetime, advisor_user_id, end_session_datetime, end_session_datetime, advisor_user_id])

        for n in record_count:
            if n.is_done == False:
                return False

        return True