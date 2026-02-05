from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from users.forms import RegisterForm,CustomRegisterForm,LoginForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse,reverse_lazy
from tasks.models import Event,Category,RSVP
from users.models import CustomUser
from django.utils.timezone import now
from django.db.models import Q,Max,Min,Avg,Count,Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView,FormView,DeleteView,CreateView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.
from django.contrib.auth import get_user_model
User=get_user_model()

class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='accounts/update_profile.html'
    context_object_name='form'
    def get_object(self):
        return self.request.user
    
        
    def form_valid(self, form):
        form.save()
        return redirect('profile')
    
# class EditProfileView(UpdateView):
#     model=User
#     form_class=EditProfileForm
#     template_name='accounts/update_profile.html'
#     context_object_name='form'
#     def get_object(self):
#         return self.request.user
#     def get_form_kwargs(self):
#         kwargs=super().get_form_kwargs()
#         kwargs['userprofile']=UserProfile.objects.get(user=self.request.user)
#         return kwargs
    
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         user_profile=UserProfile.objects.get(user=self.request.user)
#         context['form']=self.form_class(instance=self.object,userprofile=user_profile)
#         return context
#     def form_valid(self, form):
#         form.save(commit=True)
#         return redirect('profile')
    
def rsvp_event(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    try:
        RSVP.objects.create(user=request.user,event=event)
        messages.success(request,'You have successfully RSVP to this event')
    except IntegrityError:
        messages.warning(request,'Sorry,You have already RSVP to this event')
    return redirect('participant_dashboard')
        
        
class is_admin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Admin').exists()

    login_url = 'no_permission'
def is_admin_user(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()
class is_organizer(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Organizer').exists()

    login_url = 'no_permission'
# def is_participant(user):
#     return user.groups.filter(name='User').exists()
class is_participant(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Participant').exists()

    login_url = 'no_permission'

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
    
# def sign_up(request):
#     if request.method=="GET":
#         form=CustomRegisterForm()
#     if request.method=="POST":
        
#         form=CustomRegisterForm(request.POST)
#         if form.is_valid():
#             # username=form.cleaned_data.get('username')
#             # password=form.cleaned_data.get('password1')
#             # confirm_password=form.cleaned_data('password2')
#             # if password==confirm_password:
#             #     User.objects.create(username,password)
#             user=form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password'))
#             user.is_active=False
#             user.save()
            
#             messages.success(request,'A confirmation mail is Sent. Please check your email')
#             return redirect('sign_in')

#     context={
#         "form":form
#     }
#     return render(request,'registration/register.html',context)
class sign_up(FormView):
    template_name='registration/register.html'
    form_class=CustomRegisterForm
    success_url=reverse_lazy('sign_in')
    def form_valid(self, form):
        user=form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active=False
        user.save()
            
        messages.success(self.request,'A confirmation mail is Sent. Please check your email')
        return super().form_valid(form)
    
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
class CustomLogin(LoginView):
    form_class=LoginForm
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url

        
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Admin').exists():
            return reverse_lazy('admin_dashboard')
        elif user.groups.filter(name='Organizer').exists():
            return reverse_lazy('organizer_dashboard')
        else:
            return reverse_lazy('participant_dashboard')
# @login_required
# def sign_out(request):
#     if request.method=="POST":
#         logout(request)
    
#         return redirect('sign_in')


class sign_out(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        logout(request)
        return redirect('sign_in')
    

    
# @receiver(post_save,sender=User)

# def assign_role(sender,instance,created,**kwargs):
#     if created:
#         user_group,created=Group.objects.get_or_create(name='User')
#         instance.groups.add(user_group)
#         instance.save()
        
# @user_passes_test(is_admin,login_url='no_permission')
# def admin_dashboard(request):
#     users=User.objects.prefetch_related(
#         Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
#         ).all()
#     for user in users:
#         if user.all_groups:
#             user.group_name=user.all_groups[0].name
#         else:
#             user.group_name='No group assigned'
#     return render(request,'admin/dashboard.html',{"users":users})

class admin_dashboard(is_admin,TemplateView):
    template_name='admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        users=User.objects.prefetch_related(
            Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
            ).all()
        for user in users:
            if user.all_groups:
                user.group_name=user.all_groups[0].name
            else:
                user.group_name='No group assigned'
        context['users']=users
        return context
   
@user_passes_test(is_admin_user,login_url='no_permission')
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

# @user_passes_test(is_admin,login_url='no_permission')
# def create_group(request):
#     form=CreateGroupForm()
#     if request.method=="POST":
#         form=CreateGroupForm(request.POST)
#         if form.is_valid():
#             group=form.save()
#             messages.success(request,f'Group {group.name} has been created Successfully')
#             return redirect('create_group')
#     return render(request,'admin/create_group.html',{"form":form})

class create_group(is_admin,CreateView):
    template_name='admin/create_group.html'
    success_url=reverse_lazy('create_group')
    form_class=CreateGroupForm
    def form_valid(self, form):
        group=form.save()
        messages.success(self.request,f'Group {group.name} has been created Successfully')
        
        return super().form_valid(form)
    
    
# @user_passes_test(is_admin,login_url='no_permission')
# def group_list(request):
#     groups=Group.objects.all()
#     return render(request,'admin/group_list.html',{"groups":groups})


class group_list(is_admin,ListView):
    model=Group
    template_name='admin/group_list.html'
    context_object_name='groups'

# @user_passes_test(is_admin,login_url='no_permission')
# def delete_participant(request,participant_id):
#     user=get_object_or_404(User,id=participant_id)
#     if user.is_superuser:
#         messages.error(request,'Sorry,You do not have access')
#         return redirect('admin_dashboard')
#     elif request.method=="POST":
#         user.delete()
#         messages.success(request,'User successfully deleted')
    
#     return redirect('admin_dashboard')


class delete_participant(UserPassesTestMixin,View):
    login_url='no_permission'
    
    def test_func(self):
        return self.request.user.is_superuser
    def post(self,request,participant_id):
        user=get_object_or_404(User,id=participant_id)
        if user.is_superuser:
            messages.error(request,'Sorry,You do not have access')
            return redirect('admin_dashboard')
        else:
            user.delete()
            messages.success(request,'User successfully deleted')
    
        
    
        return redirect('admin_dashboard')

# @user_passes_test(is_admin,login_url='no_permission')
# def delete_group(request,group_id):
#     group=get_object_or_404(Group,id=group_id)
#     if request.method=="POST":
#         group.delete()
#         messages.success(request,'Group successfully deleted')
#     return redirect('group_list')

class delete_group(UserPassesTestMixin,View):
    login_url='no_permission'
    def test_func(self):
        return self.request.user.is_superuser
    def post(self,request,group_id):
        group=get_object_or_404(Group,id=group_id)
    
        group.delete()
        messages.success(request,'Group successfully deleted')
        return redirect('group_list')
# @user_passes_test(is_participant,login_url='no_permission')
# def participant_dashboard(request):
#     today = now().date()
#     filter_type = request.GET.get("type", "all")

#     base_query = Event.objects.select_related("category").prefetch_related("participant")

    
#     counts = Event.objects.aggregate(
#         total_event=Count("id",distinct=True),
#         upcoming_event=Count("id", filter=Q(date__gt=today),distinct=True),
#         past_event=Count("id", filter=Q(date__lt=today),distinct=True),
#         today_event=Count("id", filter=Q(date=today),distinct=True),
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

#     return render(request, "participant/participant_dashboard.html", context)




class participant_dashboard(LoginRequiredMixin,is_participant,ListView):
    model=Event
    template_name='participant/participant_dashboard.html'
    login_url='no_permission'
    context_object_name='events'
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
        context=super().get_context_data(**kwargs)
        today = now().date()
        filter_type = self.request.GET.get("type", "all")
        counts = Event.objects.aggregate(
            total_event=Count("id",distinct=True),
            upcoming_event=Count("id", filter=Q(date__gt=today),distinct=True),
            past_event=Count("id", filter=Q(date__lt=today),distinct=True),
            today_event=Count("id", filter=Q(date=today),distinct=True),
            # total_participant=Count("participant",distinct=True)
        )

    
    
        context["counts"]=counts
        context["filter_type"]=filter_type
        context["participants"]=None
        
        return context

   

class ProfileView(TemplateView):
    template_name='accounts/profile.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['bio']=user.bio
        context['profile_image']=user.profile_image
        context['member_since']=user.date_joined
        context['last_login']=user.last_login
        return context
    

class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class=CustomPasswordChangeForm
    success_url=reverse_lazy('profile')


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/password_reset.html'
    success_url=reverse_lazy('sign_in')
    html_email_template_name='registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A reset email sent. Please check your email')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='registration/password_reset.html'
    success_url=reverse_lazy('sign_in')
    def form_valid(self, form):
        messages.success(self.request,'Password has been reset successfully')
        return super().form_valid(form)
    