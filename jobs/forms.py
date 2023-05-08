from django import forms
from .models import Freelancer, Business, Project


class BusinessUpdateForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = ['name', 'profile_pic', 'about']

class FreelancerUpdateForm(forms.ModelForm):

    class Meta:
        model = Freelancer
        fields = ['name', 'profile_pic', 'skills', 'about']

class ProjectDateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'category', 'programming_languages', 'due_date', 'budjet']
        widgets = {
            'due_date': ProjectDateInput()
        }


