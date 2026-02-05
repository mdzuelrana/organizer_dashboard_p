from django.urls import path
from .views import organizer_dashboard,create_event,event_task,view_details,delete_event,update_event,load_data,ViewDetails
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('organizer_dashboard/',organizer_dashboard.as_view(),name='organizer_dashboard'),
    # path('create_event/',create_event,name='create_event'),
    path('create_event/',create_event.as_view(),name='create_event'),
    path('event_task/',event_task.as_view(),name='event_task'),
    path('view_details/<int:id>/',view_details.as_view(),name='view_details'),
    path('delete_event/<int:id>/',delete_event.as_view(),name='delete_event'),
    path('update_event/<int:id>/',update_event.as_view(),name='update_event'),
    # path('create_admin/',create_admin,name='create_admin'),
    path('load-data/',load_data, name='load_data'),

]