
# Create your views here.
from rest_framework import generics, permissions

from adminPanel.serializer import ListUsersInfoSerializer, UserSerializer, RateSerializer
from login.models import User, Reservation, Invitation
from login.serializer import CreateInvitationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView



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