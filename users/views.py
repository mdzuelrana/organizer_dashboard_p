from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from users.forms import RegisterForm,CustomRegisterForm,LoginForm,AssignRoleForm,CreateGroupForm
from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from tasks.models import Event,Category,RSVP
from django.utils.timezone import now
from django.db.models import Q,Max,Min,Avg,Count,Prefetch
# Create your views here.
def rsvp_event(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    try:
        RSVP.objects.create(user=request.user,event=event)
        messages.success(request,'You have successfully RSVP to this event')
    except IntegrityError:
        messages.warning(request,'Sorry,You have already RSVP to this event')
    return redirect('participant_dashboard')
        
        
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='User').exists()

def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('User not Found')
    
def sign_up(request):
    if request.method=="GET":
        form=CustomRegisterForm()
    if request.method=="POST":
        
        form=CustomRegisterForm(request.POST)
        if form.is_valid():
            # username=form.cleaned_data.get('username')
            # password=form.cleaned_data.get('password1')
            # confirm_password=form.cleaned_data('password2')
            # if password==confirm_password:
            #     User.objects.create(username,password)
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active=False
            user.save()
            
            messages.success(request,'A confirmation mail is Sent. Please check your email')
            return redirect('sign_in')

    context={
        "form":form
    }
    return render(request,'registration/register.html',context)

def sign_in(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if is_admin(user):
                return redirect('admin_dashboard')
            elif is_organizer(user):
                return redirect('organizer_dashboard')
            else:
                return redirect('participant_dashboard')
        
    return render(request,'registration/login.html',{"form":form})
@login_required
def sign_out(request):
    if request.method=="POST":
        logout(request)
    
        return redirect('sign_in')
    

    
@receiver(post_save,sender=User)

def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group,created=Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()
        
@user_passes_test(is_admin,login_url='no_permission')
def admin_dashboard(request):
    users=User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
        ).all()
    for user in users:
        if user.all_groups:
            user.group_name=user.all_groups[0].name
        else:
            user.group_name='No group assigned'
    return render(request,'admin/dashboard.html',{"users":users})
@user_passes_test(is_admin,login_url='no_permission')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm()
    if request.method=="POST":
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f'User {user.username} assigned to the role {role.name}')
            return redirect('admin_dashboard')
    return render(request,'admin/assign_role.html',{"form":form})

@user_passes_test(is_admin,login_url='no_permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method=="POST":
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} has been created Successfully')
            return redirect('create_group')
    return render(request,'admin/create_group.html',{"form":form})
    
@user_passes_test(is_admin,login_url='no_permission')
def group_list(request):
    groups=Group.objects.all()
    return render(request,'admin/group_list.html',{"groups":groups})

@user_passes_test(is_admin,login_url='no_permission')
def delete_participant(request,participant_id):
    user=get_object_or_404(User,id=participant_id)
    if user.is_superuser:
        messages.error(request,'Sorry,You do not have access')
        return redirect('admin_dashboard')
    elif request.method=="POST":
        user.delete()
        messages.success(request,'User successfully deleted')
    
    return redirect('admin_dashboard')

@user_passes_test(is_admin,login_url='no_permission')
def delete_group(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    if request.method=="POST":
        group.delete()
        messages.success(request,'Group successfully deleted')
    return redirect('group_list')

@user_passes_test(is_participant,login_url='no_permission')
def participant_dashboard(request):
    today = now().date()
    filter_type = request.GET.get("type", "all")

    base_query = Event.objects.select_related("category").prefetch_related("participant")

    
    counts = Event.objects.aggregate(
        total_event=Count("id",distinct=True),
        upcoming_event=Count("id", filter=Q(date__gt=today),distinct=True),
        past_event=Count("id", filter=Q(date__lt=today),distinct=True),
        today_event=Count("id", filter=Q(date=today),distinct=True),
        # total_participant=Count("participant",distinct=True)
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

    return render(request, "participant/participant_dashboard.html", context)