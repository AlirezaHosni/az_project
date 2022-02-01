
# Create your views here.
from rest_framework import generics, permissions

from adminPanel.serializer import ListUsersInfoSerializer, UserSerializer, RateSerializer
from chat.serializers import ChatListSerializer
from login.models import User, Reservation, Invitation
from chat.models import Chat_User, Chat
from login.serializer import CreateInvitationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone



class CreateUserByAdmin(generics.CreateAPIView):
    serializer_class = UserSerializer
  #  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class DeleteUserByAdmin(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self):
        return User.objects.get(id=self.kwargs['user_id'])


class getUserInfo(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserSerializer
    def get_object(self):
        return User.objects.get(id=self.kwargs['user_id'])

class ListUsersInfo(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.raw("select id, image, first_name, last_name, created_on from login_user")
        each_user_hours = []
        for user in users:
            data_reservation_datetime = Reservation.objects.raw("SELECT id, reservation_datetime, end_session_datetime FROM login_reservation where user_id=%s", [user.id])
            records_result = []
            sum_of_serssion_hours = 0
            for rec in data_reservation_datetime:
                records_result.append(int(rec.end_session_datetime.hour - rec.reservation_datetime.hour))
            for i in records_result:
                sum_of_serssion_hours += i
            each_user_hours.append({
                "id":user.id,
                "image":str(user.image),
                "first_name":user.first_name,
                "last_name":user.last_name,
                "created_on":str(user.created_on),
                "hour_of_session": sum_of_serssion_hours
            })
            sum_of_serssion_hours = 0
        
        return Response({
            "users": each_user_hours
        })


class AdvisorInvitations(APIView):
    def get(self, request, *args, **kwargs):
        advisors = User.objects.raw("select u.id, a.id as advisor_id, image, first_name, last_name from login_user as u inner join login_advisor as a on u.id = a.user_id")
        advisors_list = []
        for adv in advisors:
            data_reservation_datetime = Invitation.objects.raw("SELECT id, COUNT(id) as num_of_inv FROM login_invitation where advisor_id=%s", [adv.advisor_id])
            
            advisors_list.append({
                "advisor_id":adv.advisor_id,
                "image": str(adv.image),
                "first_name":adv.first_name,
                "last_name":adv.last_name,
                "num_of_invitation": data_reservation_datetime[0].num_of_inv
            })

        return Response({
            "advisors_list":advisors_list
        })


class ListInvitationForAdmin(APIView):
    def get(self, request, *args, **kwargs):
        invs = Invitation.objects.raw("select i.id, invitation_content, created_at, image, first_name, last_name FROM login_invitation as i inner join login_user as u on i.student_id = u.id where i.advisor_id=%s",[self.kwargs['advisor_id']])
        list = []
        for inv in invs:
            list.append({
                "image":str(inv.image),
                "invitation_content":inv.invitation_content,
                "first_name":inv.first_name,
                "last_name":inv.last_name,
                "created_on":str(inv.created_at)
            })
        return Response({
            "particular_invitations":list
        })

class DeleteParticularInvitationByAdmin(generics.DestroyAPIView):
    
    def get_object(self):
        return Invitation.objects.get(id=self.kwargs['invitation_id'])


class ListAdvisorChat(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.raw("select u.id, a.id as advisor_id, image, first_name, last_name from login_user as u inner join login_advisor as a on u.id = a.user_id")
        each_user_hours = []
        for user in users:
            data_reservation_datetime = Reservation.objects.raw("SELECT id, reservation_datetime, end_session_datetime FROM login_reservation where user_id=%s", [user.id])
            records_result = []
            sum_of_serssion_hours = 0
            for rec in data_reservation_datetime:
                records_result.append(int(rec.end_session_datetime.hour - rec.reservation_datetime.hour))
            for i in records_result:
                sum_of_serssion_hours += i
            each_user_hours.append({
                "id":user.id,
                "image":str(user.image),
                "first_name":user.first_name,
                "last_name":user.last_name,
                "hour_of_session": sum_of_serssion_hours
            })
            sum_of_serssion_hours = 0

        
        return Response({
            "advisor_chats":each_user_hours
        })

class RetrieveParticularAdvisorChats(generics.ListAPIView):
    serializer_class = ChatListSerializer
    def get_queryset(self):
        chats = Chat.objects.filter(chats_users__user=self.kwargs['user_id'])
        chat_users = Chat_User.objects.filter(Q(chat__in=chats))
        return chat_users.exclude(user_id=self.request.user.id).order_by('-chat__time_changed')

class ListReservationDetails(APIView):

    def get(self, request, *args, **kwargs):
        res = Reservation.objects.all()
        result_list = []
        for r in res:
            advisor = User.objects.raw("select u.id, image, first_name, last_name from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s", [r.advisor_user_id])
            user = User.objects.get(id=r.user_id)
            st=""
            if(timezone.now() >= r.reservation_datetime and timezone.now() <= r.end_session_datetime):    
                st = "در حال انجام"
            elif(timezone.now() < r.reservation_datetime):
                st = "رزرو شده"
            elif(timezone.now() > r.end_session_datetime):
                st = "به انمام رسیده"
            result_list.append({
                "advisor_image": str(advisor[0].image),
                "advisor_first_name":advisor[0].first_name,
                "advisor_last_name":advisor[0].last_name,
                "user_image":str(user.image),
                "user_first_name":user.first_name,
                "user_last_name":user.last_name,
                "reserve_date":str(r.created_at.date()),
                "session_status":st
            })

        return Response({
            "result":result_list
        })

class DeleteReservationByAdmin(generics.DestroyAPIView):
    def get_object(self):
        return Reservation.objects.get(id=self.kwargs['reservation_id'])