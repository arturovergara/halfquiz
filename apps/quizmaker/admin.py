# Django Imports
from django.contrib import admin

from .models import Game, GameQuestion, Option, Question, Quiz, Topic


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (OptionInline,)
    list_display = ("statement", "topic")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(Topic)
admin.site.register(GameQuestion)
