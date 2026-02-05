from django import forms
from django.forms import widgets
from .models import Event,Category
from django.contrib.auth import get_user_model
User=get_user_model()
# from django.contrib.auth.models import User
# class StyledFormMixin:
#     # default_classes="border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
#     default_classes = (
#         "w-full px-4 py-2 rounded-lg shadow-sm border border-gray-300 rounded-lg "
#         "focus:outline-none focus:ring-2 focus:ring-rose-500 "
#         "focus:border-rose-500"
#     )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_styled_widgets()
        
#     def apply_styled_widgets(self):
#         for field_name,field in self.fields.items():
#             if isinstance(field.widget,(widgets.TextInput,widgets.EmailInput,widgets.PasswordInput,)):
#                 field.widget.attrs.update({
#                     "class": self.default_classes,
#                     "placeholder": f"Enter {field.label}",
#                 })
#             elif isinstance(field.widget,forms.CharField):
#                 field.widget.attrs.update({
#                     'class':self.default_classes,
#                     'placeholder':f"Enter{field.label.lower()}"
#                 })
#             elif isinstance(field.widget,forms.Textarea):
#                 field.widget.attrs.update({
#                     'class':self.default_classes,
#                     'placeholder':f"Enter{field.label.lower()}"
#                 })
#             elif isinstance(field.widget,widgets.TimeInput):
#                 field.widget.attrs.update({
#                     'class':self.default_classes,
#                     'placeholder':f"Enter{field.label.lower()}"
#                 })
            
#             elif isinstance(field.widget,forms.SelectDateWidget):
#                 field.widget.attrs.update({
#                     'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
                    
#                 })
#             elif isinstance(field.widget,forms.CheckboxSelectMultiple):
#                 field.widget.attrs.update({
#                     'class':"space-y-2"
                    
#                 })
#             else: 
#                 field.widget.attrs.update({
#                     'class':self.default_classes
                    
#                 })


class StyledFormMixin:
    default_classes = (
        "w-full px-4 py-2 rounded-lg shadow-sm border border-gray-300 "
        "focus:outline-none focus:ring-2 focus:ring-rose-500 "
        "focus:border-rose-500"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():

            # Text-like inputs
            if isinstance(field.widget, (widgets.TextInput, widgets.EmailInput, widgets.PasswordInput, widgets.NumberInput)):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label}",
                })

            # Textarea
            elif isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 4,
                })

            # Time / Date inputs
            elif isinstance(field.widget, (widgets.TimeInput, widgets.DateInput, widgets.DateTimeInput)):
                field.widget.attrs.update({
                    "class": self.default_classes,
                })

            # Select dropdown
            elif isinstance(field.widget, widgets.Select):
                field.widget.attrs.update({
                    "class": self.default_classes,
                })

            # Checkbox multiple
            elif isinstance(field.widget, widgets.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2",
                })

            # Fallback
            else:
                field.widget.attrs.update({
                    "class": self.default_classes,
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
        self.fields['participant'].queryset = User.objects.filter(is_staff=False,is_superuser=False).distinct()
        self.apply_styled_widgets()


    

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"