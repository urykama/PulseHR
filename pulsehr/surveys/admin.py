from django.contrib import admin
from .models import Survey, Question, Choice, Answer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'is_anonymous', 'created_at']
    list_filter = ['is_active', 'is_anonymous']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey', 'question_type', 'order']
    list_filter = ['question_type', 'survey']
    inlines = [ChoiceInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'employee', 'created_at']
    list_filter = ['question__survey']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']