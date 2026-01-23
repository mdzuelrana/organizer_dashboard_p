from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,participant_dashboard,rsvp_event,delete_group,delete_participant
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign_up/',sign_up,name='sign_up'),
    path('sign_in/',sign_in,name='sign_in'),
    path('sign_out/',sign_out,name='logout'),
    path('participant/dashboard/',participant_dashboard,name='participant_dashboard'),
    path('admin/dashboard/',admin_dashboard,name='admin_dashboard'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate_user'),
    path('admin/<int:user_id>/assign_role/',assign_role,name='assign_role'),
    path('admin/create_group/',create_group,name='create_group'),
    path('admin/group_list/',group_list,name='group_list'),
    path('admin/delete_group/<int:group_id>',delete_group,name='delete_group'),
    path('admin/delete_participant/<int:participant_id>',delete_participant,name='delete_participant'),
    path('rsvp_event/<int:event_id>',rsvp_event,name='rsvp_event'),
]
