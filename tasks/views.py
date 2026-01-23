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
# from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
# from django.dispatch import receiver
# from django.core.mail import send_mail
# Create your views here.

def home(request):
    return HttpResponse('What are you doing?')
def load_data(request):
    call_command('loaddata', 'initial_data.json')
    return HttpResponse("Data loaded successfully!")
@user_passes_test(is_admin,login_url='no_permission')
def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin1234"
        )
        return HttpResponse("Superuser created")
    return HttpResponse("Superuser already exists")

@user_passes_test(is_organizer,login_url='no_permission')
def update_event(request,id):
    event=Event.objects.get(id=id)
    update_form=EventForm(instance=event)
    if request.method=="POST":
        update_form=EventForm(request.POST,instance=event)
        if update_form.is_valid():
            update_form.save()
            messages.success(request,'Event Successfully Updated')
            return redirect('update_event',id)
    context={
        "update_form":update_form
    }
    return render(request,'includes/event_form.html',context)
@user_passes_test(is_organizer,login_url='no_permission')
def delete_event(request,id):
    if request.method=="POST":
        event=Event.objects.get(id=id)
        event.delete()
        messages.success(request,'Event deleted Successfully')
        return redirect('dashboard')
    else:
        messages.error(request,'Something went wrong')
        return redirect('dashboard')
    
@user_passes_test(is_organizer,login_url='no_permission')  
def view_details(request,id):
    event=get_object_or_404(Event.objects.select_related("category").prefetch_related("participant"),id=id)
    context={
        "event":event
        
    }
    return render(request,"includes/view_details.html",context)
# def dashboard(request):
    
    
def search_view(request):
    name=request.GET.get('q','')
    events=Event.objects.filter(
        Q(name__icontains=name) | Q(location__icontains=name)
    )
    context={
        "events":events,
        'filter_type': f"search results for '{name}'"
        
    }
    return render(request,"includes/event_search.html",context)

def event_task(request):
    today = now().date()
    filter_type = request.GET.get("type", "all")

    base_query = Event.objects.select_related("category").prefetch_related("participant")

    
    counts = Event.objects.aggregate(
        total_event=Count("id"),
        upcoming_event=Count("id", filter=Q(date__gt=today)),
        past_event=Count("id", filter=Q(date__lt=today)),
        today_event=Count("id", filter=Q(date=today)),
        total_participant=Count("participant",distinct=True)
    )

    
    if filter_type == "upcoming":
        events = base_query.filter(date__gt=today)
        participants=None
    elif filter_type == "past":
        events = base_query.filter(date__lt=today)
        participants=None
    elif filter_type == "today":
        events = base_query.filter(date=today)
        participants=None
    
    else:
        events = base_query.all()
        participants=None

    context = {
        "events": events,
        "counts": counts,
        "filter_type": filter_type,
        "participants":participants
    }
    return render(request,"includes/event_task.html",context)
# def dashboard(request):
#     type=request.GET.get('type','all')
#     today=now().date()
#     total_event=Event.objects.all().count()
#     total_participant=Participant.objects.count()
#     upcoming_event=Event.objects.filter(date__gt=today).count()
#     past_event=Event.objects.filter(date__lt=today).count()
    
#     context={
#         "total_event":total_event,
#         "total_participant":total_participant,
#         "upcoming_event":upcoming_event,
#         "past_event":past_event
#     }
    
#     return render(request,"includes/organizer_dashboard.html",context)


@user_passes_test(is_organizer,login_url='no_permission')
def organizer_dashboard(request):
    today = now().date()
    filter_type = request.GET.get("type", "all")

    base_query = Event.objects.select_related("category").prefetch_related("participant")

    
    counts = Event.objects.aggregate(
        total_event=Count("id",distinct=True),
        upcoming_event=Count("id", filter=Q(date__gt=today),distinct=True),
        past_event=Count("id", filter=Q(date__lt=today),distinct=True),
        today_event=Count("id", filter=Q(date=today),distinct=True),
        total_participant=Count("participant",distinct=True)
    )

    
    if filter_type == "upcoming":
        events = base_query.filter(date__gt=today)
        participants=None
    elif filter_type == "past":
        events = base_query.filter(date__lt=today)
        participants=None
    elif filter_type == "today":
        events = base_query.filter(date=today)
        participants=None
    
    else:
        events = base_query.all()
        participants=None

    context = {
        "events": events,
        "counts": counts,
        "filter_type": filter_type,
        "participants":participants
    }

    return render(request, "includes/organizer_dashboard.html", context)
@user_passes_test(is_organizer,login_url='no_permission')
def create_event(request):
    event_form = EventForm()

    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event created successfully")
            return redirect("create_event")

    context = {
        "event_form": event_form
    }
    return render(request, "includes/event_form.html", context)

