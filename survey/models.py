# coding=utf8
import re
import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Survey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    activited = models.BooleanField(u"当前使用的问卷")

    def __unicode__(self):
        return (self.name)

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None


class Category(models.Model):
    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey)
    required = models.BooleanField(u"邀请函中是否必须")

    def __unicode__(self):
        return (self.name)


def validate_list(value):
    '''takes a text value and verifies that there is at least one comma '''
    values = re.split(',|\n', value)
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of "
                              "choices. Choices must contain more than one item.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
    )

    text = models.TextField()
    required = models.BooleanField()
    category = models.ForeignKey(Category, blank=True, null=True,)
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(
        max_length=200, choices=QUESTION_TYPES, default=TEXT)
    # the choices field is only used if the question type
    choices = models.TextField(blank=True, null=True, 
                               help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or 
                self.question_type == Question.SELECT or 
                self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.'''
        # choices = self.choices.split(',')
        choices = re.split(',|\n', self.choices)
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return (self.text)


class TrackPeople(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(u"备注", blank=True, null=True)
    slug = models.CharField(u'特殊人物', max_length=36, blank=True, null=True,
                            db_index=True, default=lambda: uuid.uuid4().hex)

    def __unicode__(self):
        return ("TrackPeople:%s %s" % (self.slug, (self.extra and self.extra.split('\n')[0] or "")))



class Response(models.Model):
    # a response object is just a collection of questions and answers with a
    # unique interview uuid
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)
    name = models.CharField(u'姓名', max_length=400)
    phone_number = models.CharField(u'电话', max_length=20)
    email = models.EmailField(u'邮箱', max_length=400)
    interview_uuid = models.CharField(u"标识符", max_length=36)
    real_ip = models.IPAddressField(u"IP", blank=True, null=True)
    browser = models.CharField(u"浏览器", max_length=200, blank=True, null=True)
    extra = models.TextField(u"备注", blank=True, null=True)
    slug = models.ForeignKey(TrackPeople)

    def __unicode__(self):
        return ("response %s" % self.interview_uuid)


class AnswerBase(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.


class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)
