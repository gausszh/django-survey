from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from models import Survey, Category, TrackPeople
from forms import ResponseForm


def Index(request):
    return render(request, 'index.html')


def SurveyDetail(request, id):
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    if request.method == 'POST':
        form = ResponseForm(data=request.POST, survey=survey, request=request)
        # form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)

    else:
        form = ResponseForm(survey=survey)
        slug = request.GET.get("slug")
        track_id = request.GET.get("track_id")
        # TODO sort by category
    return render(request, 'survey.html', 
                  {'response_form': form, 'survey': survey, 
                   'categories': categories, "slug": slug, "track_id": track_id})


def Confirm(request, uuid):
    email = settings.support_email
    return render(request, 'confirm.html', {'uuid': uuid, "email": email})


def privacy(request):
    return render(request, 'privacy.html')


def invite_index(request, slug):
    survey = Survey.objects.filter(activited=True).first()
    user = TrackPeople.objects.filter(slug=slug).first()
    if survey:
        form = ResponseForm(survey=survey)
        track = TrackPeople
        category_items = Category.objects.filter(survey=survey, required=True)
        categories = [c.name for c in category_items]
        url = "%s?track_id=%s&slug=%s" % (reverse(SurveyDetail, args=[survey.id]),
                                          user and user.id or "", 
                                          user and user.slug or "")
        return render(request, "invite.html", {'response_form': form, 
                                               'survey': survey, "url": url,
                                               'categories': categories,})

    return render(request, "invite.html")

