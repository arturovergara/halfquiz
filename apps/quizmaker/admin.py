# Django Imports
from django.contrib import admin

from .models import Game, Option, Question, Quiz, Topic


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = (OptionInline,)
    list_display = ("statement", "topic")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(Topic)
admin.site.register(Game)
