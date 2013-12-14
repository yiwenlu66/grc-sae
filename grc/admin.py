from django.contrib import admin
from grc.models import Group, Question

class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name_en','name_ch','enabled']})
    ]

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['q_class','group','title','question','answer']})
    ]


admin.site.register(Group, GroupAdmin)
admin.site.register(Question, QuestionAdmin)
