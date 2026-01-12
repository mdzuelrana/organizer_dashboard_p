from django.urls import path
from .views import dashboard,create_event,event_task,search_view,view_details,delete_event,update_event,create_admin,load_data
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('create_event/',create_event,name='create_event'),
    path('event_task/',event_task,name='event_task'),
    path('view_details/<int:id>/',view_details,name='view_details'),
    path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('update_event/<int:id>/',update_event,name='update_event'),
    path('create_admin/',create_admin,name='create_admin'),
    path('load-data/',load_data, name='load_data'),

]