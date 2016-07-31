# coding=utf8
from survey.models import (Question, Category, Survey, Response, AnswerText, 
                           AnswerRadio, AnswerSelect, AnswerInteger, 
                           AnswerSelectMultiple, TrackPeople)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('category',)
    extra = 0

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0

class SurveyAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, QuestionInline]

class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    readonly_fields = ('question',)
    extra = 0

class AnswerTextInline(AnswerBaseInline):
    model= AnswerText  

class AnswerRadioInline(AnswerBaseInline):
    model= AnswerRadio 

class AnswerSelectInline(AnswerBaseInline):
    model= AnswerSelect 

class AnswerSelectMultipleInline(AnswerBaseInline):
    model= AnswerSelectMultiple

class AnswerIntegerInline(AnswerBaseInline):
    model= AnswerInteger 

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'interview_uuid', 'name', 'created') 
    inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline]
    # specifies the order as well as which fields to act on 
    readonly_fields = ('survey', 'created', 'updated', 'interview_uuid', "slug")


class TrackPeopleAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'extra', 'invite') 
    def invite(self, track):
        url = " /invite/%s/" % track.slug
        return u'<a href="%s" target="blank">点击查看邀请函</a>' % url
    invite.short_description = u"邀请函"
    invite.allow_tags = True


# admin.site.register(Question, Questioninline)
# admin.site.register(category, categoryInline)
admin.site.register(Survey, SurveyAdmin)

admin.site.register(Response, ResponseAdmin)
admin.site.register(TrackPeople, TrackPeopleAdmin)