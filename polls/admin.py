from django.contrib import admin

from .models import Poll, Question


class PoolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'time_start', 'time_end', 'description')
    search_fields = ('text', 'time_start')
    list_filter = ('time_start',)
    empty_value_display = '-пусто-'


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'type')
    search_fields = ("text", )
    list_filter = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Poll, PoolAdmin)
admin.site.register(Question, QuestionAdmin)