from django import forms
from django.forms import Form
from diary.models import Diary, Entry


class DiaryForm(forms.ModelForm):
    class Meta:
         model = Diary
         fields = ['user','name','description']   
         
class DiaryEditForm(forms.ModelForm):
    class Meta:
         model = Diary
         fields = ['name','description']      
         
class EntryForm(forms.ModelForm):
    class Meta:
         model = Entry
         fields = ['diary','title','body']