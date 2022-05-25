from django.core.mail import message
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from chat.models import Chat_User
from login.models import AdvisorDailyTime, Rate, Email_Verification, Reservation, User, Advisor
from datetime import timedelta
from .serializer import ReservationSerializer
from datetime import datetime
import json


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
            if (chat_user.is_done == False):
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
    message = "این نظر قبلا تایید شده است و امکان ویرایش نیست"

    def has_permission(self, request, view):
        try:
            rate = Rate.objects.filter(id=view.kwargs['id']).first()
            if (rate.is_confirmed == True):
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
    message = "این بازه زمانی قبلا رزرو شده است یا در بازه کاری مشاور نیست"
    def has_permission(self, request, view):
        serialized_data = ReservationSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        reservation_datetime = serialized_data.validated_data['reservation_datetime']
        end_session_datetime = reservation_datetime + timedelta(minutes=serialized_data.validated_data['duration_min'])
        advisor_user_id = serialized_data.validated_data['receiver']
        #print(advisor_user_id)
        record_count = Reservation.objects.raw("select id, is_done from chat_chat_user where user_id in (select user_id from login_reservation where (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s) OR (reservation_datetime <= %s AND end_session_datetime >= %s AND advisor_user_id=%s))",
         [reservation_datetime, reservation_datetime, advisor_user_id, end_session_datetime, end_session_datetime, advisor_user_id])

        advisor_daily_routine = AdvisorDailyTime.objects.get(advisor__user_id = serialized_data.validated_data['receiver'])
        job_time_dump = json.dumps(advisor_daily_routine.job_time)
        job_time_dic = json.loads(job_time_dump)

        for n in record_count:
            if n.is_done == False:
                return False

        

        for d in job_time_dic:
            if reservation_datetime.date() == datetime.strptime(d['date'], '%Y-%m-%d').date():
                begin_time = datetime.strptime(d['begin_time'], '%H:%M:%S').time()
                end_time = datetime.strptime(d['end_time'], '%H:%M:%S').time()
                if reservation_datetime.time() < begin_time:
                    return False
                if end_session_datetime.time() > end_time:
                    return False
                return True
            return False
        return False
        # if advisor_daily_routine.job_time == None or advisor_daily_routine.job_time == None:
        #     return False

        # if reservation_datetime.time() < advisor_daily_routine.daily_begin_time:
        #     return False

        # if end_session_datetime.time() > advisor_daily_routine.daily_end_time: 
        #     return False


class IsJobTimeExist(permissions.BasePermission):
    message = "برای این مشاور رکورد تایم کاری موجود هست. از همین اندپوینت با متد پوت یا پچ استفاده شود"

    def has_permission(self, request, view):
        try:
            advisor_id = Advisor.objects.get(user_id=request.user.id).id
            a = AdvisorDailyTime.objects.get(advisor_id=advisor_id)

        except(AdvisorDailyTime.DoesNotExist):
            return True
        return False
