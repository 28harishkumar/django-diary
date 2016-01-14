from django.contrib import admin

from diary.models import Diary, Entry

admin.site.register(Diary)
admin.site.register(Entry)

