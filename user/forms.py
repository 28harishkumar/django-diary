from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import *

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email",
        error_messages={'invalid': "This value may contain only letters, numbers and @/. characters."},
        widget = forms.EmailInput(attrs={'placeholder': 'It will be your username/identity',
                                             'onblur':'checkemail(this.value)'}))
    class Meta(UserCreationForm.Meta):
        model = User
        UserCreationForm.Meta.fields = ("username","email","first_name")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("This email address is already in database. Use forget password to reset your password.")
    
class RegisterUserForm(MyUserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email','password1',
                  'password2','is_active','confirmation_code']
        
    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name")).strip()
        if first_name == '':
            raise forms.ValidationError("first name required")
        return first_name
    
    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()

        return user
  