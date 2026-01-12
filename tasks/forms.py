from django import forms
from django.forms import widgets
from .models import Event,Participant,Category

class StyledFormMixin:
    default_classes="border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            
            if isinstance(field.widget,forms.CharField):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,widgets.TimeInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
                    
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                    
                })
            else: 
                field.widget.attrs.update({
                    'class':self.default_classes
                    
                })
        
class EventForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Event
        fields="__all__"
        widgets={
            "participant":forms.CheckboxSelectMultiple(),
            "category":forms.Select(),
            "date":forms.SelectDateWidget(),
            "time":forms.TimeInput(format="%I:%M %p",attrs={"type": "time"})
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['participant'].queryset = Participant.objects.filter(participant__isnull=False).distinct()
        self.apply_styled_widgets()

class ParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields="__all__"
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"