from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Event

@receiver(m2m_changed,sender=Event.participant.through)
def notify_task_creation(sender,instance,action,**kwargs):
    if action=="post_add":
        participant_emails=[emp.email for emp in instance.participant.all()]
        send_mail(
            "New Event assigned",
            f"You have been assigned to the event: {instance.name}",
            "mail",
            participant_emails,
            fail_silently=False,
        )
        
        

