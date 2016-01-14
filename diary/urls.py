from django.conf.urls import include, url
from diary.views import *

urlpatterns = [
    url(r'^$',DiaryList.as_view(),name='diary_list'),
    url(r'^diary/new$',NewDiary.as_view(),name='new_diary'),
    url(r'^diary/(?P<diary_id>[0-9]+)/edit',EditDiary.as_view(),name='edit_diary'),
    url(r'^diary/(?P<diary_id>[0-9]+)/delete$',DeleteDiary.as_view(),name='delete_diary'),
    url(r'^(?P<diary_id>[0-9]+)/$',DiaryHome.as_view(),name='diary_home'),
    url(r'^(?P<diary_id>[0-9]+)/entry/(?P<entry_id>[0-9]+)/$',EntryView.as_view(),name='diary_entry'),
    url(r'^(?P<diary_id>[0-9]+)/entry/new/$',NewEntry.as_view(),name='new_diary_entry'),
    url(r'^entry/(?P<entry_id>[0-9]+)/delete$',DeleteEntry.as_view(),name='delete_entry'),
    url(r'^search$',SearchEntry.as_view(),name='search_entry'),
    ]