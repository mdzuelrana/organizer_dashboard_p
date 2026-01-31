from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from tasks.models import RSVP
from users.models import CustomUser
from django.contrib.auth import get_user_model
User=get_user_model()
@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token=default_token_generator.make_token(instance)
        activation_url=f'{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/'
        subject="Active Your Account"
        message=f'Hi {instance.username},\n\nPlease activate your account by clicking the link below \n\n{activation_url}\n\n Thank You'

        recipient_list=[instance.email]
        # try:
        print("EMAIL:", instance.email)
        print("FROM:", settings.EMAIL_HOST_USER)
        send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list,fail_silently=True,)
            
        # except Exception as e:
            
        #     print(f"Failed to send email at {instance.email}: {e}")



@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = "Event RSVP Confirmation"
        message = f"""
            Hi {instance.user.username},

            You have successfully RSVP’d to the event:

            Name: {instance.event.name}
            Date: {instance.event.date}
            Location: {instance.event.location}
            Time: {instance.event.time}

            Thank you for participating!
            """
        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.user.email],
                fail_silently=True,
            )

# @receiver(post_save,sender=User)
# def create_update_user_profile(sender,instance,created,**kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     # instance.userprofile.save()