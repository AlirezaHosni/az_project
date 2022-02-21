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
from .models import AdvisorDailyTime, Notifiaction, Email_Verification, Advisor, Reservation, User, Request, Rate, Advisor_History, Advisor_Document , Invitation
from .permissions import IsJobTimeExist, CanReserveDatetime, CanBeActive, IsAdvisor, IsChatDone, IsChatExist, IsNotConfirmed
from .serializer import AdvJobTimeSerializer, AdvisorAdvSerializer, ReservationAdvSerializer, UpdateFileStatusSerializer, ListAdvisorInfoForAdminSerializer, UploadSerializer, reservedSessionSerializer, ReservationSerializer, UserVerificationSerializer, UpdateRateSerializer, AdvisorDocSerializer, RateFinderSerializer, AdvisorInfoSerializer, professionFinder, \
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
from chat.models import Chat_User, Chat
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
        activate_link_url = "https://moshaver.markop.ir/login/"
        actiavation_link = f'{activate_link_url}?user_id={UserSerializer(user).data["id"]}&confirmation_token={confirmation_token}'
        # send an e-mail to the user
        context = "لطفا برای فعالسازی حساب خود به لینک زیر مراجعه کنید" + '\n' + str(actiavation_link)

        send_mail(
            # title:
            "فعالسازی حساب کاربری در مشاوره آنلاین",
            # message:
            context,
            # from:
            "ostadmoshaverteam@gmail.com",
            # to:
            [UserSerializer(user).data["email"]]
        )

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
        # User.objects.filter(id=user.id).update(last_login=datetime.datetime.now())
        user.last_login=datetime.datetime.now()
        cf = user.email_confirmed_at
        user.save()
        return Response({'token': token.key,
        "email_confirmed_at":str(cf)})

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
    permission_classes = (permissions.IsAuthenticated,)


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
            'select res.user_id as user_id,res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone, res.is_verified from login_rate as r right join (select a.id,u.id as user_id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone, is_verified from login_user as u inner join login_advisor as a on u.id = a.user_id) as res on advisor_id =res.id group by res.id order by rate desc')

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

        oldNotifiactions = Notifiaction.objects.filter(Q(user=self.request.user.id) & Q(seen=False)).order_by('-created_at')
        updatedNotifiactions = oldNotifiactions

        for notification in updatedNotifiactions.iterator():
            notification.seen = True
            notification.save()
        
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
            docs.append(User.objects.raw("SELECT login_user.id, image, first_name, last_name, doc_files, doc_file, is_verified FROM login_user inner JOIN (SELECT user_id, login_advisor_document.id as doc_files, doc_file, is_verified from login_advisor inner JOIN login_advisor_document on login_advisor_document.advisor_id = login_advisor.id) as res on res.user_id = login_user.id where login_user.id=%s ORDER BY id", [user.id]))
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
                    "doc_files_ext": file_ext_each[i],
                    "is_verified":docs[i][0].is_verified
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
        data_gender_male = User.objects.raw("select id from login_user where gender='M'")
        data_gender_female = User.objects.raw("select id from login_user where gender='F'")
        man_percentage = (len(data_gender_male)/(len(data_gender_male) + len(data_gender_female)))*100
        woman_percentage = (len(data_gender_female)/(len(data_gender_male) + len(data_gender_female)))*100
        # print(man_percentage)
        # print(woman_percentage)
        data_daily_view = User.objects.raw("select id from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 DAY)")
        data_monthly_view = User.objects.raw("select id from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 MONTH)")
        data_yearly_view = User.objects.raw("select id from login_user where last_login <= (CURDATE() + INTERVAL 1 DAY) AND last_login >= (CURDATE() - INTERVAL 1 YEAR)")
        # print(data_daily_view[0].num)
        daily_user = []
        daily_advisor = []
        for i in range(0, 31):
            data_daily_advisor_joined = User.objects.raw("select u.id from login_user as u where u.created_on <= (CURDATE() - INTERVAL %s DAY) AND u.created_on >= (CURDATE() - INTERVAL %s DAY) AND u.is_advisor=1",[i, i+1])
            daily_advisor.append(len(data_daily_advisor_joined))

        for i in range(0, 31):
            data_daily_user_joined = User.objects.raw("select u.id from login_user as u where u.created_on <= (CURDATE() - INTERVAL %s DAY) AND u.created_on >= (CURDATE() - INTERVAL %s DAY) AND u.is_advisor=0",[i, i+1])
            daily_user.append(len(data_daily_user_joined))
        # print(data_monthly_view[0].num)
        # data_daily_joined = User.objects.raw("select id from login_user where created_on <= (CURDATE() + INTERVAL 1 DAY) AND created_on >= (CURDATE() - INTERVAL 1 DAY)")
        # data_monthly_joined = User.objects.raw("select id from login_user where created_on <= (CURDATE() + INTERVAL 1 DAY) AND created_on >= (CURDATE() - INTERVAL 1 MONTH)")
        # data_yearly_joined = User.objects.raw("select id from login_user where created_on <= (CURDATE() + INTERVAL 1 DAY) AND created_on >= (CURDATE() - INTERVAL 1 YEAR)")
        # print(data_yearly_view[0].num)
        data_completed_session = User.objects.raw("SELECT id from chat_chat_user where CURDATE() >= end_session_datetime")

        data_reserved_session = User.objects.raw("SELECT id from login_reservation")

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
            "daily_view":len(data_daily_view),
            "monthly_view":len(data_monthly_view),
            "yearly_view":len(data_yearly_view),
            "completed_session": len(data_completed_session)/2,
            "reserved_session": len(data_reserved_session),
            "session_hours":int(sum_of_serssion_hours),
            "daily_user_joined":daily_user,
            "daily_advisor_joined":daily_advisor
        })



class VerifyAdvisor(generics.UpdateAPIView):
    serializer_class = AdvisorSerializer

    def get_object(self):
        return Advisor.objects.get(user_id=self.kwargs['user_id'])

class AdvProfileByAdvId(APIView):
    # serializer_class = AdvisorAdvSerializer

    def get(self, request, *args, **kwargs):
        a = Advisor.objects.raw("select u.id, a.id as advisor_id, first_name,last_name,email,year_born,phone_number,gender,image, is_verified, daily_begin_time, daily_end_time,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where a.id=%s", [self.kwargs['advisor_id']])
        g = Advisor_History.objects.filter(advisor_id=a[0].advisor_id)
        arr=[]
        for i in g:
            arr.append(i.granted_prize)

        return Response({
            "id": a[0].id,
            "advisor_id": a[0].advisor_id,
            "first_name": a[0].first_name,
            "last_name": a[0].last_name,
            "phone_number": a[0].phone_number,
            "is_verified": a[0].is_verified,
            "daily_begin_time": a[0].daily_begin_time,
            "daily_end_time": a[0].daily_end_time,
            "telephone": a[0].telephone,
            "address": a[0].address,
            "advise_method": a[0].advise_method,
            "meli_code": a[0].meli_code,
            "is_ejucation_advisor": a[0].is_ejucation_advisor,
            "is_healthcare_advisor": a[0].is_healthcare_advisor,
            "is_sport_advisor": a[0].is_sport_advisor,
            "is_family_advisor": a[0].is_family_advisor,
            "is_mental_advisor": a[0].is_mental_advisor,
            "granted_prize": arr
        })
            


class ResendVerificationEmail(APIView):
    def post(self, request):
        # serializer = RegisterSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        confirmation_token = Email_Verification.objects.get(user_id=request.user.id).key
        #print(confirmation_token)
        #print(UserSerializer(user).data['id'])
        #token = Token.objects.get(user).key
        activate_link_url = "https://moshaver.markop.ir/login/"
        actiavation_link = f'{activate_link_url}?user_id={request.user.id}&confirmation_token={confirmation_token}'
        # send an e-mail to the user
        context = "لطفا برای فعالسازی حساب خود به لینک زیر مراجعه کنید" + '\n' + str(actiavation_link)

        send_mail(
            # title:
            "فعالسازی حساب کاربری در مشاوره آنلاین",
            # message:
            context,
            # from:
            "ostadmoshaverteam@gmail.com",
            # to:
            [request.user.email]
        )

        return Response({
            "Result":"ایمیل تایید مجددا ارسال شد!"
        })


class ListAdvisorReservation(generics.ListAPIView):
    serializer_class = ReservationAdvSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Reservation.objects.raw("select r.id, r.user_id, r.advisor_user_id, r.chat_id ,reservation_datetime, end_session_datetime, created_at, first_name, last_name from login_reservation as r inner join login_user as u on r.user_id=u.id where r.advisor_user_id=%s order by reservation_datetime", [self.request.user.id])
    # def get(self, request):
    #     reses = Reservation.objects.filter(advisor_user_id=self.kwargs['advisor_user_id'])
    #     io = []
    #     for res in reses:
    #         date_time_b = res.reservation_datetime
    #         datetime_b = self.gregorian_to_jalali(date_time_b.year, date_time_b.month, date_time_b.day)
    #         date_time_e = res.end_session_datetime
    #         datetime_e = self.gregorian_to_jalali(date_time_e.year, date_time_e.month, date_time_e.day)
    #         io.append({
    #             "id":res.id,
    #             "reservation_datetime":"%s-%s-%s ",
    #             "end_session_datetime":res.end_session_datetime,
    #             "created_at":res.created_at,
    #             "advisor_user_id":res.advisor_user_id,
    #             "user_id":res.user_id
    #         })
    #     return Response()

    # def gregorian_to_jalali(gy, gm, gd):
    #     g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    #     if (gm > 2):
    #         gy2 = gy + 1
    #     else:
    #         gy2 = gy
    #         days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    #         jy = -1595 + (33 * (days // 12053))
    #         days %= 12053
    #         jy += 4 * (days // 1461)
    #         days %= 1461
    #     if (days > 365):
    #         jy += (days - 1) // 365
    #         days = (days - 1) % 365
    #     if (days < 186):
    #         jm = 1 + (days // 31)
    #         jd = 1 + (days % 31)
    #     else:
    #         jm = 7 + ((days - 186) // 30)
    #         jd = 1 + ((days - 186) % 30)
    #     return [jy, jm, jd]


class DeleteReservedSessionByAdvisor(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            # advisor = Advisor.objects.get(user_id=self.kwargs['user_id'])
            # Advisor.objects.filter(user_id=self.kwargs['user_id']).delete()
            # User.objects.filter(id=advisor.user_id).delete()
            res = Reservation.objects.get(id=self.kwargs['reservation_id'])
            Chat_User.objects.filter(chat_id=res.chat_id).delete()
            Chat.objects.filter(id=res.chat_id).delete()
            res.delete()

            return Response({
                "message": "رزرو حذف شد"
            })
        except(Chat_User.DoesNotExist):
            return Response({
                "message":"چنین رزروی وجود ندارد"
            })


class ListAdvisorReservationByAdvId(generics.ListAPIView):
    serializer_class = ReservationAdvSerializer
    def get_queryset(self):
        return Reservation.objects.raw("select r.id, r.user_id, r.advisor_user_id, r.chat_id ,reservation_datetime, end_session_datetime, created_at, first_name, last_name from login_reservation as r inner join login_user as u on r.user_id=u.id where r.advisor_user_id=%s order by reservation_datetime", [self.kwargs['advisor_user_id']])
   

class CreateAdvJobTime(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsJobTimeExist]
    serializer_class = AdvJobTimeSerializer

class RetrieveUpdateJobTime(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvJobTimeSerializer
    def get_object(self):
        advisor_id = Advisor.objects.get(user_id=self.request.user.id).id
        return AdvisorDailyTime.objects.get(advisor_id=advisor_id)