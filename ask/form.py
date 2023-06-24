from .models import Question, Answer, Profile, Image
from django import forms
from django.contrib.auth.models import User

class QForm (forms.ModelForm):
    title=forms.CharField(label='Title(optional)',required=None, widget=forms.TextInput(attrs={'style':'', 'class':'form-control'}))
    body=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Ask a Question', 'class':'form-control', 'style':''}))
    class Meta:
        model=Question
        fields=['title', 'body']
        require=None
        
class AForm(forms.ModelForm):
    body=forms.CharField(label='', required=False, widget=forms.Textarea(attrs={'placeholder':'Input Text', 'class':'form-control'}))
    
    class Meta:
        model=Answer
        fields=['body']
        #use_required_attribute=False
        
class PForm(forms.ModelForm):
    
    class Meta:
        model=Profile
        fields=['age' , 'islam']   

class UForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name']
        
    