from django.db import models
from django.contrib.auth import get_user_model
from django.conf import Settings

User=get_user_model()
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    
    def __str__(self):
        return self.name


    
    
class Event(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    participant=models.ManyToManyField(User,through='RSVP',related_name='participant')
    #participant=models.ManyToManyField(Settings.AUTH_USER_MODEL,through='RSVP',related_name='participant')
    def __str__(self):
        return self.name
    
class RSVP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #user=models.ForeignKey(Settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    rsvp_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user','event')
    
    def __str__(self):
        return f'{self.user.username} and {self.event.name}'
    
    

    
    










    
# class Task(models.Model):
#     STATUS_CHOICES=[
#         ('PENDING','Pending'),
#         ('IN_PROGRESS','In Progress'),
#         ('COMPLETED','Completed')
#     ]
#     project=models.ForeignKey(Project,on_delete=models.CASCADE,default=1)
#     assigned_to=models.ManyToManyField(Employee,related_name='tasks')
#     title=models.CharField(max_length=200)
#     description=models.TextField()
#     due_date=models.DateField()
#     status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='PENDING')
#     is_completed=models.BooleanField(default=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.title

# class TaskDetail(models.Model):
#     HIGH='H'
#     MEDIUM='M'
#     LOW='L'
#     PRIORITY_OPTIONS=(
#         (HIGH,'High'),
#         (MEDIUM,'Medium'),
#         (LOW,'Low')
#     )
#     # std_id=models.CharField(max_length=200,primary_key=True)
#     task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name='details')
#     # assigned_to=models.CharField(max_length=100)
#     priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
#     notes=models.TextField(blank=True,null=True)
#     def __str__(self):
#         return f'task detail{self.task.title}'


