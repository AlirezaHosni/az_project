from django.urls import path

from adminPanel.views import DeleteParticularInvitationByAdmin, ListInvitationForAdmin, AdvisorInvitations, ListUsersInfo, CreateUserByAdmin, DeleteUserByAdmin, getUserInfo

urlpatterns = [
    path('create-user/', CreateUserByAdmin.as_view()),
    path('delete-user/<int:user_id>/', DeleteUserByAdmin.as_view()),
    path('get-user-info/<int:user_id>/', getUserInfo.as_view()),
    path('list-users/', ListUsersInfo.as_view()),
    path('list-advisors-invitation/', AdvisorInvitations.as_view()),
    path('list-particular-invitations/<int:advisor_id>/', ListInvitationForAdmin.as_view()),
    path('delete-invitation-by-admin/<int:invitation_id>/', DeleteParticularInvitationByAdmin.as_view()),

]