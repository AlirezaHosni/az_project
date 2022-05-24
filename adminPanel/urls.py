from django.urls import path

from adminPanel.views import RetrieveAdvisorInfo, createAdvisor, getAdvisorList, DeleteAdvisor, ListRate, ListParticularUserRates, UpdateCommentStatus, DeleteReservationByAdmin, ListReservationDetails, ListAdvisorChat, RetrieveParticularAdvisorChats, DeleteParticularInvitationByAdmin, ListInvitationForAdmin, AdvisorInvitations, ListUsersInfo, CreateUserByAdmin, DeleteUserByAdmin, getUserInfo

urlpatterns = [
    path('create-user/', CreateUserByAdmin.as_view()),
    path('delete-user/<int:user_id>/', DeleteUserByAdmin.as_view()),
    path('get-user-info/<int:user_id>/', getUserInfo.as_view()),
    path('list-users/', ListUsersInfo.as_view()),
    # path('list-advisors-invitation/', AdvisorInvitations.as_view()),
    # path('list-particular-invitations/<int:advisor_id>/', ListInvitationForAdmin.as_view()),
    # path('delete-invitation-by-admin/<int:invitation_id>/', DeleteParticularInvitationByAdmin.as_view()),
    path('retrieve-particular-advisor-chats/<int:user_id>/', RetrieveParticularAdvisorChats.as_view()),
    path('list-advisors-chat/', ListAdvisorChat.as_view()),
    path('list-reservation-details/', ListReservationDetails.as_view()),
    path('delete-reservation/<int:reservation_id>', DeleteReservationByAdmin.as_view()),
    
    path('delete-or-update-comment-status/<int:rate_id>/', UpdateCommentStatus.as_view()),
    path('list-particular-user-rates/<int:advisor_id>/', ListParticularUserRates.as_view()),
    path('list-users-rates/', ListRate.as_view()),#
    path('delete-advisor/<int:user_id>/', DeleteAdvisor.as_view()),
    path('list-advisors/', getAdvisorList.as_view()),
    path('create-advisors/', createAdvisor.as_view()),
    path('get-advisor-info/<int:advisor_id>/', RetrieveAdvisorInfo.as_view()),



]