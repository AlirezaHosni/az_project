
# Create your views here.
from rest_framework import generics, permissions

from adminPanel.serializer import  AdvChatSer, ReservationSerializer, RateSerializer, createAdvisorSerializer, ListUsersInfoSerializer, UserSerializer, RateSerializer
from chat.serializers import ChatListSerializer
from login.models import Advisor, User, Reservation, Invitation, Rate
from chat.models import Chat_User, Chat
from login.serializer import CreateInvitationSerializer, AdvisorSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone



class CreateUserByAdmin(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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
            data_reservation_datetime = Invitation.objects.raw("SELECT id, COUNT(id) as num_of_inv FROM login_invitation where advisor_id=%s group by id", [adv.advisor_id])
            
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
            data_reservation_datetime = Reservation.objects.raw("SELECT id, reservation_datetime, end_session_datetime FROM login_reservation where advisor_user_id=%s", [user.id])
            records_result = []
            sum_of_serssion_hours = 0
            for rec in data_reservation_datetime:
                records_result.append(abs(int(rec.end_session_datetime.hour - rec.reservation_datetime.hour)))
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

class RetrieveParticularAdvisorChats(APIView):
    def get(self, request, *args, **kwargs):
        chats = Chat_User.objects.raw("select c.id ,user_id, chat_start_datetime, end_session_datetime, time_changed, title from chat_chat_user as cu inner join chat_chat as c on c.id=cu.chat_id where user_id=%s", [self.kwargs['user_id']])
        objs = []
        for chat in chats:
            contact = User.objects.raw("select * from login_user where id in (select user_id from chat_chat_user where chat_id=%s and user_id !=%s)", [chat.id, chat.user_id])
            for con in contact:
                objs.append({
                    "chat": {
                        "chat_id": chat.id, 
                        "title": chat.title,
                        "time_changed": str(chat.time_changed),
                        "chat_start_datetime": str(chat.chat_start_datetime),
                        "end_session_datetime":str(chat.end_session_datetime)
                    },
                    "contact":{
                        "id": con.id,
                        "email": con.email,
                        "first_name": con.first_name,
                        "last_name": con.last_name,
                        "email_confirmed_at": str(con.email_confirmed_at),
                        "phone_number": con.phone_number,
                        "status":con.status
                    }
                })
        return Response(objs)
        # chats = Chat.objects.filter(chats_users__user=self.kwargs['user_id'])
        # chat_users = Chat_User.objects.filter(Q(chat__in=chats))
        # return chat_users.exclude(user_id=self.request.user.id).order_by('-chat__time_changed')

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
                "advisor_id":advisor[0].id,
                "advisor_image": str(advisor[0].image),
                "advisor_first_name":advisor[0].first_name,
                "advisor_last_name":advisor[0].last_name,
                "user_id":user.id,
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


class createAdvisor(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = createAdvisorSerializer


class getAdvisorList(APIView):
    def get(self, request, *args, **kwargs):
        # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        users = User.objects.raw("select res.user_id as id, res.id as advisor_id ,res.user_id as user_id, res.created_on, COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name from login_rate as r right join (select a.id,u.id as user_id,created_on,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id) as res on advisor_id =res.id group by res.id order by rate desc")
        each_user_hours = []
        for user in users:
            data_reservation_datetime = Reservation.objects.raw("SELECT id, reservation_datetime, end_session_datetime FROM login_reservation where advisor_user_id=%s", [user.user_id])
            records_result = []
            sum_of_serssion_hours = 0
            for rec in data_reservation_datetime:
                records_result.append(abs(int(rec.end_session_datetime.hour - rec.reservation_datetime.hour)))
            for i in records_result:
                sum_of_serssion_hours += i
            each_user_hours.append({
                "advisor_id":user.advisor_id,
                "user_id":user.user_id,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "created_on":str(user.created_on),
                "hour_of_session": sum_of_serssion_hours,
                "rate":user.rate
            })
            sum_of_serssion_hours = 0

        return Response(each_user_hours)


class DeleteAdvisor(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            advisor = Advisor.objects.get(user_id=self.kwargs['user_id'])
            Advisor.objects.filter(user_id=self.kwargs['user_id']).delete()
            User.objects.filter(id=advisor.user_id).delete()

            return Response({
                "message": "مشاور حذف شد"
            })
        except(Advisor.DoesNotExist):
            return Response({
                "message":"چنین مشاوری وجود ندارد"
            })



class ListRate(APIView):
    def get(self, request, *args, **kwargs):
        users = Rate.objects.all()
        us = []
        for i in users:
            user_rates = Rate.objects.filter(advisor_id=i.advisor_id)
            num_of_rates = len(user_rates)
            user = User.objects.raw("select u.id, u.id as user_id, a.id as advisor_id, first_name, last_name from login_user as u inner join login_advisor as a on u.id=a.user_id where a.id=%s",[i.advisor_id])
            us.append({
                "id":user[0].id,
                "user_id":user[0].user_id,
                "advisor_id":user[0].advisor_id,
                "num_of_rates":num_of_rates,
                "first_name":user[0].first_name,
                "last_name":user[0].last_name
            })
        return Response({
            "users":us
        })

class ListParticularUserRates(APIView):
    def get(self, request, *args, **kwargs):
        rates = Rate.objects.filter(advisor_id=self.kwargs['advisor_id'])
        us = []
        for rate in rates:
            # advisor = Advisor.objects.get(id=rate.advisor_id)
            user = User.objects.get(id=rate.user_id)
            us.append({
                "user_id":user.id,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "gender": user.gender,
                "email": user.email,
                "phone_number": user.phone_number,
                "year_born": user.year_born,
                "rate_id":rate.id,
                "text":rate.text,
                "rate_created_on":rate.created_at,
                "rate":rate.rate,
                "is_confirmed":rate.is_confirmed
            })

        return Response({
            "rates":us
        })

class UpdateCommentStatus(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RateSerializer
    def get_object(self):
        return Rate.objects.get(id=self.kwargs['rate_id'])


class RetrieveAdvisorInfo(generics.RetrieveAPIView):
    serializer_class = AdvisorSerializer
    def get_object(self):
        return Advisor.objects.get(id=self.kwargs['advisor_id'])





    
