from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils.timezone import now
from tasks.forms import EventForm,CategoryForm
from tasks.models import Event,Category
from datetime import date
from django.db.models import Q,Max,Min,Avg,Count
from users.views import is_organizer,is_admin
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,UpdateView,DetailView,TemplateView,CreateView,DeleteView
from django.urls import reverse_lazy
# from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
# from django.dispatch import receiver
# from django.core.mail import send_mail
# Create your views here.
create_decorators=[login_required,permission_required('is_organizer',login_url='no_permission')]
# def home(request):
#     return HttpResponse('What are you doing?')

class home(View):
    def get(self,request):
        return HttpResponse('What are you doing?')

def load_data(request):
    call_command('loaddata', 'initial_data.json')
    return HttpResponse("Data loaded successfully!")
# @user_passes_test(is_admin,login_url='no_permission')
# def create_admin(request):
#     if not User.objects.filter(username="admin").exists():
#         User.objects.create_superuser(
#             username="admin",
#             email="admin@example.com",
#             password="admin1234"
#         )
#         return HttpResponse("Superuser created")
#     return HttpResponse("Superuser already exists")

# @user_passes_test(is_organizer,login_url='no_permission')
# def update_event(request,id):
#     event=Event.objects.get(id=id)
#     update_form=EventForm(instance=event)
#     if request.method=="POST":
#         update_form=EventForm(request.POST,instance=event)
#         if update_form.is_valid():
#             update_form.save()
#             messages.success(request,'Event Successfully Updated')
#             return redirect('update_event',id)
#     context={
#         "update_form":update_form
#     }
#     return render(request,'includes/event_form.html',context)

class update_event(is_organizer,UpdateView):
    model=Event
    form_class=EventForm
    template_name='includes/event_form.html'
    context_object_name='event'
    pk_url_kwarg='id'
    login_url='no_permission'
    def form_valid(self, form):
        messages.success(self.request, 'Event successfully updated')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('update_event', kwargs={'id': self.object.id})
    
    # def get_context_data(self, **kwargs):
        
    #     context = super().get_context_data(**kwargs)
    #     context["event_form"] = self.get_form()
    #     return context
        
    # def post(self,request,*args,**kwargs):
    #     self.object=self.get_object()
    #     update_form=EventForm(request.POST,instance=self.object)
    #     if update_form.is_valid():
    #         update_form.save()
    #         messages.success(request,'Event Successfully Updated')
    #         return redirect('update_event',self.object.id)
    #     return redirect('update_event',self.object.id)
        
    
# @user_passes_test(is_organizer,login_url='no_permission')
# def delete_event(request,id):
#     if request.method=="POST":
#         event=get_object_or_404(Event,id=id)
#         event.delete()
#         messages.success(request,'Event deleted Successfully')
#         return redirect('organizer_dashboard')
#     else:
#         messages.error(request,'Something went wrong')
#         return redirect('organizer_dashboard')


class delete_event(is_organizer,DeleteView):
    model=Event
    pk_url_kwarg='id'
    login_url='no_permission'
    
    success_url = reverse_lazy('organizer_dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Event deleted successfully')
        return super().form_valid(form)

    
    
    # def post(self,request,id,*args,**kwargs):
    #     event=get_object_or_404(Event,id=id)
    #     event.delete()
    #     messages.success(request,'Event deleted Successfully')
    #     return redirect('organizer_dashboard')
    # def get(self,request,*args,**kwargs):
    #     messages.error(request,'Something went wrong')
    #     return redirect('organizer_dashboard')
    
# @user_passes_test(is_organizer,login_url='no_permission')  
# def view_details(request,id):
#     event=get_object_or_404(Event.objects.select_related("category").prefetch_related("participant"),id=id)
#     context={
#         "event":event
        
#     }
#     return render(request,"includes/view_details.html",context)

class view_details(is_organizer,DetailView):
    model=Event
    template_name='includes/view_details.html'
    login_url='no_permission'
    context_object_name='event'
    pk_url_kwarg='id'
    def get_queryset(self):
         
        return Event.objects.select_related("category").prefetch_related("participant")
    
    

view_details_decorators=[login_required,permission_required('is_organizer',login_url='no_permission')]
@method_decorator(view_details_decorators,name='dispatch')
class ViewDetails(ListView):
    model=Event
    context_object_name='event'
    template_name='includes/view_details.html'
    def get_queryset(self):
        queryset=get_object_or_404(Event.objects.select_related("category").prefetch_related("participant"),id=id)
        return queryset

    
# def search_view(request):
#     name=request.GET.get('q','')
#     events=Event.objects.filter(
#         Q(name__icontains=name) | Q(location__icontains=name)
#     )
#     context={
#         "events":events,
#         'filter_type': f"search results for '{name}'"
        
#     }
#     return render(request,"includes/event_search.html",context)
class search_view(ListView):
    model=Event
    template_name='includes/event_search.html'
    context_object_name='events'
    def get_queryset(self):
        name=self.request.GET.get('q','')
        return Event.objects.filter(Q(name__icontains=name) | Q(location__icontains=name))
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        name=self.request.GET.get('q','')
    
        context["filter_type"]=f"search results for '{name}'"
        return context

# def event_task(request):
#     today = now().date()
#     filter_type = request.GET.get("type", "all")

#     base_query = Event.objects.select_related("category").prefetch_related("participant")

    
#     counts = Event.objects.aggregate(
#         total_event=Count("id"),
#         upcoming_event=Count("id", filter=Q(date__gt=today)),
#         past_event=Count("id", filter=Q(date__lt=today)),
#         today_event=Count("id", filter=Q(date=today)),
#         # total_participant=Count("participant",distinct=True)
#     )

    
#     if filter_type == "upcoming":
#         events = base_query.filter(date__gt=today)
#         participants=None
#     elif filter_type == "past":
#         events = base_query.filter(date__lt=today)
#         participants=None
#     elif filter_type == "today":
#         events = base_query.filter(date=today)
#         participants=None
    
#     else:
#         events = base_query.all()
#         participants=None

#     context = {
#         "events": events,
#         "counts": counts,
#         "filter_type": filter_type,
#         "participants":participants
#     }
#     return render(request,"includes/event_task.html",context)
class event_task(ListView):
    model=Event
    template_name='includes/event_task.html'
    login_url='no_permission'
    context_object_name="events"
    
    
    
    def get_queryset(self):
        
        today = now().date()
        filter_type = self.request.GET.get("type", "all")

        base_query = Event.objects.select_related("category").prefetch_related("participant")
        if filter_type == "upcoming":
            return base_query.filter(date__gt=today)
            
        elif filter_type == "past":
            return base_query.filter(date__lt=today)
            
        elif filter_type == "today":
            return base_query.filter(date=today)
            
        
        else:
            return base_query.all()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        today = now().date()
        filter_type = self.request.GET.get("type", "all")
        counts = Event.objects.aggregate(
            total_event=Count("id"),
            upcoming_event=Count("id", filter=Q(date__gt=today)),
            past_event=Count("id", filter=Q(date__lt=today)),
            today_event=Count("id", filter=Q(date=today)),
            # total_participant=Count("participant",distinct=True)
        )

    
    
        context["counts"]=counts
        context["filter_type"]=filter_type
        
        context["participants"]=None
        
        return context
    
def dashboard(request):
    type=request.GET.get('type','all')
    today=now().date()
    total_event=Event.objects.all().count()
    total_participant=Participant.objects.count()
    upcoming_event=Event.objects.filter(date__gt=today).count()
    past_event=Event.objects.filter(date__lt=today).count()
    
    context={
        "total_event":total_event,
        "total_participant":total_participant,
        "upcoming_event":upcoming_event,
        "past_event":past_event
    }
    
    return render(request,"includes/organizer_dashboard.html",context)



class organizer_dashboard(is_organizer,TemplateView):
    template_name='includes/organizer_dashboard.html'
    login_url='no_permission'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
         
    
        today = now().date()
        filter_type = self.request.GET.get("type", "all")

        base_query = Event.objects.select_related("category").prefetch_related("participant")
        if filter_type == "upcoming":
            events= base_query.filter(date__gt=today)
        
        elif filter_type == "past":
            events= base_query.filter(date__lt=today)
            
        elif filter_type == "today":
            events= base_query.filter(date=today)
            
        
        else:
            events= base_query.all()
           

    
        counts = Event.objects.aggregate(
            total_event=Count("id",distinct=True),
            upcoming_event=Count("id", filter=Q(date__gt=today),distinct=True),
            past_event=Count("id", filter=Q(date__lt=today),distinct=True),
            today_event=Count("id", filter=Q(date=today),distinct=True),
            # total_participant=Count("participant",distinct=True)
        )

    
    

        context = {
            "events": events,
            "counts": counts,
            "filter_type": filter_type,
            "participants":None
        }
        return context

    
# @user_passes_test(is_organizer,login_url='no_permission')
# def create_event(request):
#     event_form = EventForm()

#     if request.method == "POST":
#         event_form = EventForm(request.POST)
#         if event_form.is_valid():
#             event_form.save()
#             messages.success(request, "Event created successfully")
#             return redirect("create_event")

#     context = {
#         "event_form": event_form
#     }
#     return render(request, "includes/event_form.html", context)

class create_event(is_organizer,CreateView):
    model=Event
    template_name='includes/event_form.html'
    login_url='no_permission'
    form_class = EventForm
    success_url=reverse_lazy('create_event')

    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Event created successfully")
        return super().form_valid(form)
        
            
    
# @method_decorator(create_decorators,name="dispatch")
# class CreateEvent(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
#     permission_required='is_organizer'
#     login_url='sign_in'
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['event_form']=kwargs.get('event_form',EventForm())
#         return context
    
#     def get(self,request,*args,**kwargs):
#         event_form = EventForm()

    

#         context = self.get_context_data()
#         return render(request, "includes/event_form.html", context)
#     def post(self,request,*args,**kwargs):
        

        
#             form = EventForm()
#             def form_valid(self, form):
#                 form.save()
#                 messages.success(request, "Event created successfully")
#                 return super().form_valid(form)
            
#                 event_form.save()
#                 messages.success(request, "Event created successfully")
#                 return redirect("create_event")

        
#         return render(request, "includes/event_form.html", context)
        