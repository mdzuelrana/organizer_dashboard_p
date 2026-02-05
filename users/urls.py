from django.urls import path
from users.views import sign_up,sign_in,CustomLogin,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,participant_dashboard,rsvp_event,delete_group,delete_participant,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView,PasswordChangeDoneView,PasswordChangeView
urlpatterns = [
    path('sign_up/',sign_up.as_view(),name='sign_up'),
    # path('sign_in/',sign_in,name='sign_in'),
    path('sign_in/',CustomLogin.as_view(),name='sign_in'),
    # path('sign_out/',sign_out,name='logout'),
    path('sign_out/',LogoutView.as_view(),name='logout'),
    path('participant/dashboard/',participant_dashboard.as_view(),name='participant_dashboard'),
    path('admin/dashboard/',admin_dashboard.as_view(),name='admin_dashboard'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate_user'),
    path('admin/<int:user_id>/assign_role/',assign_role,name='assign_role'),
    path('admin/create_group/',create_group.as_view(),name='create_group'),
    path('admin/group_list/',group_list.as_view(),name='group_list'),
    path('admin/delete_group/<int:group_id>',delete_group.as_view(),name='delete_group'),
    path('admin/delete_participant/<int:participant_id>',delete_participant.as_view(),name='delete_participant'),
    path('rsvp_event/<int:event_id>',rsvp_event,name='rsvp_event'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('password_change/',ChangePassword.as_view(),name='password_change'),
    path('password_change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password_reset/',CustomPasswordResetView.as_view(),name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit_profile/',EditProfileView.as_view(),name='edit_profile')
]   
