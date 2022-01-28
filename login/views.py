import datetime
from re import search
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from yaml.tokens import FlowEntryToken
from .models import Notifiaction, Email_Verification, Advisor, Reservation, User, Request, Rate, Advisor_History, Advisor_Document , Invitation
from .permissions import CanReserveDatetime, CanBeActive, IsAdvisor, IsChatDone, IsChatExist, IsNotConfirmed
from .serializer import UpdateFileStatusSerializer, ListAdvisorInfoForAdminSerializer, UploadSerializer, reservedSessionSerializer, ReservationSerializer, UserVerificationSerializer, UpdateRateSerializer, AdvisorDocSerializer, RateFinderSerializer, AdvisorInfoSerializer, professionFinder, \
    AdvisorResumeSerializer, ListRateSerializer, RateSerializer, CreateRequestSerializer, RequestUpdateSerializer, \
    RequestSerializer, SearchInfoSerializer, RegisterSerializer, UserSerializer, AdvisorSerializer, CreateInvitationSerializer, ListNotifiactionSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import filters
from django.http import HttpResponse
from .custom_renderer import JpegRenderer, PngRenderer
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.http import HttpResponse
from wsgiref.util import FileWrapper
# run this command for knox
#   pip install django-rest-knox
#   pip install drf-spectacular


class SignUpAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_token = Email_Verification.objects.get(user_id=UserSerializer(user).data["id"]).key
        #print(confirmation_token)
        #print(UserSerializer(user).data['id'])
        #token = Token.objects.get(user).key
        activate_link_url = "https://moshaver.markop.ir/"
        actiavation_link = f'{activate_link_url}?user_id={UserSerializer(user).data["id"]}&confirmation_token={confirmation_token}'
        # send an e-mail to the user
        context = "لطفا برای فعالسازی حساب خود به لینک زیر مراجعه کنید" + '\n' + str(actiavation_link)

        # send_mail(
        #     # title:
        #     "فعالسازی حساب کاربری در مشاوره آنلاین",
        #     # message:
        #     context,
        #     # from:
        #     "ostadmoshaverteam@gmail.com",
        #     # to:
        #     [UserSerializer(user).data["email"]]
        # )

        return Response({
            # "user": UserSerializer(user).data,
            #"token": Token.objects.get_or_create(UserSerializer(user).data).key
            "Result":"Registeration was successfull!"
        })


class LoginUserAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.status = 'online'
        user.save()
        return Response({'token': token.key})

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class Logout(APIView):
    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.status = 'offline'
        request.user.save()
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserInfoAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super(UserInfoAPI, self).update(request, *args, **kwargs)


class AdvisorInfoAPI(generics.RetrieveUpdateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Advisor.objects.get(user_id=self.request.user.id)


class SearchAdvisorAPI(generics.ListAPIView):
    serializer_class = SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        search_name = self.kwargs['search']
        search_list = search_name.split(" ")

        if len(search_list) <= 1:
            return User.objects.raw(
                "select res.user_id as user_id,res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where first_name like %s or last_name like %s) as res on advisor_id =res.id group by res.id order by rate desc",
                ['%' + search_list[0] + '%', '%' + search_list[0] + '%'])
        elif len(search_list) > 1:
            return User.objects.raw(
                "select res.user_id as user_id,res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time, is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time, is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where first_name like %s or last_name like %s union (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time, is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where first_name like %s or last_name like %s)) as res on advisor_id =res.id group by res.id order by rate desc",
                ['%' + search_list[0] + '%', '%' + search_list[0] + '%', '%' + search_list[1] + '%',
                 '%' + search_list[1] + '%'])


class SendRequestAPI(generics.CreateAPIView):
    serializer_class = CreateRequestSerializer
    permission_classes = (permissions.IsAuthenticated,CanReserveDatetime,CanReserveDatetime,)


class RequestsInfoAPI(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Request.objects.raw(
            'select email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id = r.sender_id where u.id = %s',
            [self.request.user.id])


class AdvisorRequestsInfoAPI(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def get_queryset(self):
    #     return Request.objects.raw(
    #         'select r.sender_id as sender_id, email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id=r.sender_id where r.receiver_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s) and is_checked=false',
    #         [self.request.user.id])

    def get_queryset(self):
        return Request.objects.filter(Q(receiver=self.request.user) & Q(is_checked=False))


class RequestUpdateStatus(generics.UpdateAPIView):
    serializer_class = RequestUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, CanReserveDatetime,)

    def get_object(self):
        return Request.objects.get(id=self.kwargs['id'])


class CreateInvitationAPI(generics.CreateAPIView):

    serializer_class = CreateInvitationSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdvisor]

    
class CreateRateAPI(generics.CreateAPIView):
    serializer_class = RateSerializer
    permission_classes = (permissions.IsAuthenticated,IsChatExist,IsChatDone,)


class ListRateAPI(generics.ListAPIView):
    serializer_class = ListRateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Rate.objects.raw(
            'select rate.id, rate.text, rate.rate, rate.created_at , user.first_name, user.last_name, user.image  from login_rate as rate inner join login_user as user on rate.user_id=user.id where rate.advisor_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s)',
            [self.request.user.id])


class ListRateByAdvisorIdAPI(generics.ListAPIView):
    serializer_class = ListRateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advisor_id = self.kwargs['advisor_id']
        return Rate.objects.raw(
            'select user.id as user_id, rate.id, rate.text, rate.rate, rate.created_at , user.first_name, user.last_name, user.image  from login_rate as rate inner join login_user as user on rate.user_id=user.id where rate.advisor_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where a.id=%s)',
            [advisor_id])

class ListRateForAdminAPI(generics.ListAPIView):
    serializer_class = ListRateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        return Rate.objects.raw(
            'select user.id as user_id, rate.id, rate.text, rate.rate, rate.created_at , user.first_name, user.last_name, user.image  from login_rate as rate inner join login_user as user on rate.user_id=user.id where rate.is_confirmed=false'
        )

class UpdateRateStatusByAdminAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateRateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsNotConfirmed]

    def get_object(self):
        return Rate.objects.get(id=self.kwargs['id'])




class ListAdvisorResumeAPI(generics.ListCreateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advisor = Advisor.objects.get(user=self.request.user.id)
        return Advisor_History.objects.raw('select id, granted_prize from login_advisor_history where advisor_id=%s',
                                           [advisor.id])


class ListAdvisorResumeByAdvisorIdAPI(generics.ListCreateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advisor_id = self.kwargs['advisor_id']
        return Advisor_History.objects.raw('select id, granted_prize from login_advisor_history where advisor_id=%s',
                                           [advisor_id])

class ListAdvisorDocsAPI(generics.ListCreateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advisor = Advisor.objects.get(user=self.request.user.id)
        return Advisor_Document.objects.raw('select id, doc_image from login_Advisor_Document where advisor_id=%s',
                                           [advisor.id])


class listAdvisorDocsByIdAPI():
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        advisor_id = self.kwargs['advisor_id']
        return Advisor_Document.objects.raw('select id, doc_image from login_Advisor_Document where advisor_id=%s',
                                           [advisor_id])


class UpdateAdvisorResumeAPI(generics.UpdateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Advisor_History.objects.get(id=self.kwargs['granted_prize_id'])


# destroy


class CreateAdvisor(generics.CreateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GetAllAdvisorsAPI(generics.ListAPIView):
    serializer_class = SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.raw(
            'select res.user_id as user_id,res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id) as res on advisor_id =res.id group by res.id order by rate desc')

    # class GetParticularAdvisorsAPI(generics.ListAPIView):


#     serializer_class = SearchInfoSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         serilized = professionFinder(data=self.request.data)
#         serilized.is_valid()
#         profession = serilized.validated_data['profession']
#         value = serilized.validated_data['value']
#         return User.objects.raw('select * from login_user as u inner join login_advisor as a on u.id = a.user_id where '+profession+' = %s', [value]) 


# class GetParticularAdvisorCommentsAPI(generics.ListAPIView):

class BestAdvisorsByProfessionAPI(generics.ListAPIView):
    serializer_class = SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        profession = self.kwargs['profession']

        return Advisor.objects.raw(
            'select res.user_id as user_id,res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where ' + profession + ' = true) as res on advisor_id =res.id group by res.id order by rate desc')


class GetUserImageAPI(APIView):

    def get(self, request):
        img = User.objects.get(id=self.request.user.id).image
        return HttpResponse(img, content_type="image/png")


class ImageApiView(generics.RetrieveAPIView):
    renderer_classes = [PngRenderer]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.get(id=self.kwargs['id']).image
        data = queryset

        return Response(data, content_type='image/png')

        # return Response(data, content_type='image/png')


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = "لطفا برای بازیابی رمز خود به لینک زیر مراجعه کنید" + '\n' + "https://moshaver.markop.ir/{}?token={}".format(
            reverse('password_reset:reset-password-request')[5:], reset_password_token.key)

        send_mail(
            # title:
            "Password Reset for {}".format('Ostad Moshaver'),
            # message:
            context,
            # from:
            "ostadmoshaverteam@gmail.com",
            # to:
            [reset_password_token.user.email]
        )


class ListParticularAdvisorDocuments(generics.ListAPIView):
    serializer_class = AdvisorDocSerializer

    def get_queryset(self):
        advisor_id = self.kwargs['advisor_id']
        return Advisor_Document.objects.raw('select * from login_advisor_document where advisor_id=%s', [advisor_id])


class ListNotificationsAPI(generics.ListAPIView):
    serializer_class = ListNotifiactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):

        oldNotifiactions = Notifiaction.objects.filter(user=self.request.user.id).order_by('-created_at')
        # updatedNotifiactions = oldNotifiactions
        # updatedNotifiactions.seen = False
        # updatedNotifiactions.save()
        
        return oldNotifiactions


class ActivateAccountAPI(generics.UpdateAPIView):
    serializer_class = UserVerificationSerializer
    permission_classes = (permissions.AllowAny, CanBeActive)

    def get_object(self):
        return User.objects.get(id=self.kwargs['user_id'])
        

class ListCreateReservation(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, CanReserveDatetime]

    # def get_queryset(self):
    #     return None

# class RequestUpdateStatus(generics.UpdateAPIView):
#     serializer_class = RequestUpdateSerializer
#     permission_classes = (permissions.IsAuthenticated, CanReserveDatetime,)

#     def get_object(self):
#         return Request.objects.get(id=self.kwargs['id'])


class ListReservedDateTimeForParticularAdvisor(generics.ListAPIView):
    serializer_class = reservedSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.raw("select id, advisor_user_id, user_id, reservation_datetime, end_session_datetime from login_reservation where DATE('reservation_datetime') >= CURDATE()")


# class InMomentReservationAPI(generics.CreateAPIView):
#     serializer_class = reservedSessionSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class Upload(generics.CreateAPIView):
#     serializer_class = UploadSerializer
#     permission_classes = [permissions.IsAuthenticated]

class UploadDocFile(generics.ListCreateAPIView):
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Advisor_Document.objects.filter(advisor_id=self.kwargs['advisor_id'])


class DownloadFileImage(APIView):
    def get(self, request, *args, **kwargs):
        file_path = Advisor_Document.objects.get(id=self.kwargs['file_id']).doc_file
        if str(file_path)[-3:] == "pdf" or str(file_path)[-3:] == "PDF":
            document = open("media/" + str(file_path), 'rb')
            response = HttpResponse(FileWrapper(document), content_type='application/pdf')
            return response
        else:
            document = open("media/" + str(file_path), 'rb')
            response = HttpResponse(FileWrapper(document), content_type='image/png')
            return response
        return None

class DownloadFilePDF(APIView):
    def get(self, request, *args, **kwargs):
        file_path = Advisor_Document.objects.get(id=self.kwargs['file_id']).doc_file
        document = open("media/" + str(file_path), 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/pdf')
        return response

class DeleteUploadedFile(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return Advisor_Document.objects.get(id=self.kwargs['file_id'])

class ListAdvisorInfoForAdmin(APIView):

    def get(self, request, *args, **kwargs):
        users = User.objects.raw("SELECT login_user.id, image, first_name, last_name FROM login_user inner JOIN (SELECT user_id from login_advisor inner JOIN login_advisor_document on login_advisor_document.advisor_id = login_advisor.id) as res on res.user_id = login_user.id Group BY id")
        docs = []
        file_ids = []
        file_ids_each = []
        file_ext = []
        file_ext_each = []
        for user in users:
            docs.append(User.objects.raw("SELECT login_user.id, image, first_name, last_name, doc_files, doc_file FROM login_user inner JOIN (SELECT user_id, login_advisor_document.id as doc_files, doc_file from login_advisor inner JOIN login_advisor_document on login_advisor_document.advisor_id = login_advisor.id) as res on res.user_id = login_user.id where login_user.id=%s ORDER BY id", [user.id]))
        for u in range(len(users)):
            for user in docs[u]:
                file_ids.append(user.doc_files)
                file_ext.append(str(user.doc_file)[-3:])
            file_ids_each.append(file_ids)
            file_ext_each.append(file_ext)
            file_ext = []
            file_ids = []

        response =[]
        for i in range(len(users)):
            response.append(
                {
                    "id": docs[i][0].id,
                    "image": str(docs[i][0].image),
                    "first_name": docs[i][0].first_name,
                    "last_name": docs[i][0].last_name,
                    "doc_files": file_ids_each[i],
                    "doc_files_ext": file_ext_each[i]
                }
            )
        #print(response)
        return Response(response)



class UpdateDocFileStatus(generics.UpdateAPIView):
    serializer_class = UpdateFileStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Advisor_Document.objects.get(id=self.kwargs['file_id'])  #it needs a boolean to compare accepted or denied.
        

class ListAnalyticalData(APIView):
    def get(self, request, *args, **kwargs):
        data_gender = User.objects.raw("select id, COUNT(id) as male_then_female from login_user group by gender")
        man_percentage = (data_gender[0].male_then_female/(data_gender[0].male_then_female + data_gender[1].male_then_female))*100
        woman_percentage = (data_gender[1].male_then_female/(data_gender[0].male_then_female + data_gender[1].male_then_female))*100
        # print(man_percentage)
        # print(woman_percentage)
        data_daily_view = User.objects.raw("select id, COUNT(id) as num from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 DAY)")
        data_monthly_view = User.objects.raw("select id, COUNT(id) as num from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 MONTH)")
        data_yearly_view = User.objects.raw("select id, COUNT(id) as num from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 YEAR)")
        # print(data_daily_view[0].num)
        # print(data_monthly_view[0].num)
        # print(data_yearly_view[0].num)
        data_completed_session = User.objects.raw("SELECT id, COUNT(id)/2 as completed_sessions from chat_chat_user where CURDATE() >= end_session_datetime")

        data_reserved_session = User.objects.raw("SELECT id, COUNT(id) as reserved from login_reservation")

        data_reservation_datetime = Reservation.objects.raw("SELECT id, reservation_datetime, end_session_datetime FROM login_reservation")
        records_result = []
        sum_of_serssion_hours = 0
        for rec in data_reservation_datetime:
            records_result.append(int(rec.end_session_datetime.hour - rec.reservation_datetime.hour))
        for i in records_result:
            sum_of_serssion_hours += i


        return Response({
            "man_percentage": man_percentage,
            "woman_percentage": woman_percentage,
            "daily_view":data_daily_view[0].num,
            "monthly_view":data_monthly_view[0].num,
            "yearly_view":data_yearly_view[0].num,
            "completed_session": data_completed_session[0].completed_sessions,
            "reserved_session": data_reserved_session[0].reserved,
            "session_hours":int(sum_of_serssion_hours)
        })