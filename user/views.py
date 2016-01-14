import random, string, datetime
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse , Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
        AdminPasswordChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
        
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings

from user.models import User
from user.forms import RegisterUserForm
        

# Create your views here.
class Home(View):
    @method_decorator(login_required)
    def get(self,request):
        return render_to_response('home.html',
                                  context_instance=RequestContext(request))
    
class Login(View):
    def reset_session_errors(self, request):
         try:
            del request.session['errors']
         except KeyError:
            pass
        
    def get(self,request):
        next = request.GET.get('next','/')
        if request.user.is_authenticated():
            return HttpResponseRedirect(next)
        form = AuthenticationForm()
        return render_to_response('registration/login.html', 
                                  {'form':form,'next': next}, 
                                  context_instance=RequestContext(request))
    
    def post(self,request):
        self.reset_session_errors(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next','/')
                return HttpResponseRedirect(next)
            else:
                request.session['errors'] = ['your account is not activated']
                return HttpResponseRedirect('/')
        else:
            request.session['errors'] = ['Invalid username and password combination',]
            return HttpResponseRedirect('/')

class Logout(View):
    def get(self,request):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect('/')

class PasswordChange(View):
    @method_decorator(login_required)
    def get(self,request):
        form = PasswordChangeForm(request.user)
        return render_to_response('registration/password_change_form.html', 
                                  {'form':form}, 
                                  context_instance=RequestContext(request))
    
    @method_decorator(login_required)
    def post(self,request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('registration/password_change_form.html', 
                                      {'form':form}, 
                                      context_instance=RequestContext(request))

class PasswordReset(View):
    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = PasswordResetForm()
        return render_to_response('registration/password_reset_form.html', 
                                  {'form':form}, 
                                  context_instance=RequestContext(request))
    
    def post(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(from_email= settings.EMAIL_HOST_USER , email_template_name='registration/password_reset_email.html', request=request)
            return HttpResponseRedirect('/')
        return render_to_response('registration/password_reset_form.html', 
                                  {'form':form}, 
                                  context_instance=RequestContext(request))

class SetPassword(View):
    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        user_id = request.GET['user_id']
        user = get_object_or_404(User, id = user_id)
        form = SetPasswordForm(user = user)
        return render_to_response('registration/set_password_form.html', 
                                  {'form':form}, 
                                  context_instance=RequestContext(request))
    
    def post(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = SetPasswordForm(data=request.POST)
        if form.is_valid():
            form.save()
            HttpResponseRedirect('/')
        return render_to_response('registration/set_password_form.html', 
                                  {'form':form}, 
                                  context_instance=RequestContext(request))

def send_registration_confirmation(user):
    title = "Find All Together Diary account confirmation"
    content = "Click on this link to verify your email address https://django-diary.herokuapp.com/confirm/" + str(user.confirmation_code) + "/" + user.email
    send_mail(title, content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def confirm(request, confirmation_code, email):
    try:
        user = User.objects.get(email=email)
        one_day_diff = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        d1 = datetime.datetime.strptime(one_day_diff.strftime("%Y-%m-%dT%H:%M"),"%Y-%m-%dT%H:%M")
        d2 = datetime.datetime.strptime(user.date_joined.strftime("%Y-%m-%dT%H:%M"),"%Y-%m-%dT%H:%M")
        if user.confirmation_code == str(confirmation_code) and d2 > d1:
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend' 
            auth.login(request, user)
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect(reverse('register_user'))
        
class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return render_to_response('registration/register.html',
                                  context_instance=RequestContext(request))
    
    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        data = request.POST.copy()
        data['active'] = False
        data['confirmation_code'] = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
        form = RegisterUserForm(data)
        
        if form.is_valid():
            user = form.save(commit= False)
            send_registration_confirmation(user)
            form.save()
            return HttpResponseRedirect(reverse('register_success'))
        return render_to_response('registration/register.html',
                                  {'form':form},
                                  context_instance=RequestContext(request))
        
class RegisterSuccess(View):
    def get(self, request):
        return render_to_response('registration/register_success.html')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
