from django.shortcuts import render , render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse , Http404
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from diary.models import Diary, Entry
from diary.forms import DiaryForm, EntryForm, DiaryEditForm

class DiaryList(View):
    @method_decorator(login_required)
    def get(self, request):
        diaries = Diary.objects.filter(user = request.user)
        return render_to_response('diary/home.html',{
                                    'diaries': diaries},
                                       context_instance=RequestContext(request))
        
class NewDiary(View):
    @method_decorator(login_required)
    def get(self, request):
        return render_to_response('diary/new.html',
                        context_instance = RequestContext(request))
    
    @method_decorator(login_required)
    def post(self,request):
        name = request.POST.get('name',None)
        if name == None:
            raise Http404()
        
        data = request.POST.copy()
        try:
            diary = Diary.objects.get(name = name)
            raise Http404()
        except:
            pass
        
        data['user'] = request.user.id
        form = DiaryForm(data)
        if(form.is_valid()):
            form.save()
            diary_id = Diary.objects.get(name=data['name']).id
            return HttpResponseRedirect(reverse('diary_home',kwargs={'diary_id':diary_id}))
        else:
            raise Http404()
        
class EditDiary(View):
    @method_decorator(login_required)
    def get(self, request, diary_id):
        diary = Diary.objects.get(pk = diary_id, user = request.user.id)
        return render_to_response('diary/new.html',
                        {'diary': diary},
                        context_instance = RequestContext(request))
    @method_decorator(login_required)
    def post(self, request, diary_id):
        name = request.POST.get('name',None)
        if name == None:
            raise Http404()
        
        data = request.POST.copy()
        try:
            diary = Diary.objects.get(pk = diary_id)
        except:
            raise Http404()
        
        if name != diary.name:        
            try:
                diary2 = Diary.objects.get(name = name)
                if diary2.id != diary.id:
                    raise Http404()
            except:
                pass
            
        form = DiaryEditForm(data, instance = diary)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('diary_home',kwargs={'diary_id':diary.id}))
        else:
            raise Http404()
    
class DeleteDiary(View):
    @method_decorator(login_required)
    def post(self, request, diary_id):
        try:
            diary = Diary.objects.get(pk = diary_id, user = request.user.id)
        except:
            raise Http404()

        try:
            diary.delete()
            return HttpResponseRedirect('/')
        except:
            raise Http404()
        
class DiaryHome(View):
    @method_decorator(login_required)
    def get(self, request, diary_id):
        diary = Diary.objects.get(pk = diary_id)
        if diary.user != request.user:
            raise Http404()
        entries = Entry.objects.filter(diary = diary_id).order_by('-timestamp')
        return render_to_response('diary/entrylist.html',{
                                'diary': diary,
                                'entries': entries},
                                context_instance=RequestContext(request))
    
class EntryView(View):
    @method_decorator(login_required)
    def get(self, request, diary_id, entry_id):
        diary = Diary.objects.get(pk = diary_id)
        if(diary.user != request.user):
            raise Http404()
        entry = Entry.objects.get(pk = entry_id, diary = diary.id)
        return render_to_response('diary/entry.html',{
                                    'diary': diary,
                                    'entry': entry
                                    },
                                  context_instance = RequestContext(request))
    
    @method_decorator(login_required)
    def post(self, request, diary_id, entry_id):
        diary = Diary.objects.get(pk = diary_id)
        print('reached here 1')
        if(diary.user != request.user):
            raise Http404()
        entry = Entry.objects.get(pk = entry_id)
        form = EntryForm(request.POST, instance = entry)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('diary_entry',kwargs={'diary_id':diary_id, 'entry_id': entry_id}))
        else:
            raise Http404()

class NewEntry(View):
    @method_decorator(login_required)
    def get(self, request, diary_id):
        diary = Diary.objects.get(pk = diary_id)
        if(diary.user != request.user):
            raise Http404()
        return render_to_response('diary/entry.html',{
                          'diary': diary,                            
                        },
                        context_instance = RequestContext(request))
    
    @method_decorator(login_required)
    def post(self,request, diary_id):
        diary = Diary.objects.get(pk = diary_id)
        if(diary.user != request.user):
            raise Http404()
        data = request.POST.copy()
        data['diary'] = diary.id
        form = EntryForm(data)
        if(form.is_valid()):
            form.save()
            entry_id = Entry.objects.get(title=data['title']).id
            return HttpResponseRedirect(reverse('diary_entry',kwargs={'diary_id':diary_id, 'entry_id': entry_id}))
        else:
            raise Http404()
        
class DeleteEntry(View):
    @method_decorator(login_required)
    def post(self, request, entry_id):
        try:
            entry = Entry.objects.get(pk = entry_id)
        except:
            raise Http404()
        
        diary = entry.diary
        
        if diary.user.id != request.user.id:
            raise Http404()
        try:
            entry.delete()
            return HttpResponseRedirect(reverse('diary_home',kwargs={ 'diary_id' : diary.id }))
        except:
            return HttpResponse('fail')
        
class SearchEntry(View):
    @method_decorator(login_required)
    def get(self, request):
        search = request.GET.get('s',None)
        if search == None:
            return HttpResponseRedirect('/')
        
        diaries = request.user.diary_set.all()        
        entries = Entry.objects.filter(title__icontains = search, diary__in = diaries).order_by('-timestamp')
        return render_to_response('diary/searchlist.html',{
                                'entries': entries},
                                context_instance=RequestContext(request))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        