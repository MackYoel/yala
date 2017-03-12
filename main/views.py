from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from .forms import PersonForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from project.settings import APP_NAME
from .models import Person, Issue, Session
from services.serializers import PersonSerializer
import json
from datetime import timedelta, datetime, timezone
# import time


@login_required
def ss(req):
    return render(req, 'main/home.html', locals())


@login_required
def home(req):
    # file_version = time.time()
    app_name = APP_NAME
    user = Person.objects.get(pk=req.user.pk)
    serializer = PersonSerializer(user, many=False)
    user = serializer.data
    return render(req, 'main/home.html', locals())


class LoginHandler(View):
    template_name = 'main/login.html'

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        app_name = APP_NAME

        if request.path == '/login/':
            return render(request, self.template_name, locals())

        return render(request, 'main/sign-up.html', locals())

    def post(self, request, *args, **kwargs):

        form = PersonForm(data=request.POST)
        if form.is_valid():
            user = form.get_or_create_user()
            login(request, user)
            if request.is_ajax():
                return HttpResponse()
            return redirect(reverse('main:home'))
        return HttpResponse(json.dumps(form.errors), content_type='application/json', status=400)  # NOQA


def logout_handler(request):
    logout(request)
    return redirect(reverse('main:LoginHandler'))


@login_required
def analitycs(req):
    today = datetime.now().replace(hour=0, minute=0, second=0)
    weekstart = today - timedelta(days=today.weekday())
    weekend = weekstart.replace(hour=23, minute=59, second=59) + timedelta(days=6)  # NOQA
    issues = Issue.objects.filter(completed_at__range=(weekstart, weekend),  person=req.user)
    data = [['Lunes', 0], ['Martes', 0], ['Miércoles', 0], ['Jueves', 0], ['Viernes', 0], ['Sábado', 0], ['Domingo', 0]]  # NOQA

    for i in issues:
        completed_at = i.completed_at.replace(tzinfo=timezone.utc).astimezone(tz=None)  # NOQA
        data[completed_at.weekday()][1] += 1

    sessions = Session.objects.filter(
        person=req.user,
        starts_at__year=today.year,
        starts_at__month=today.month,
        starts_at__day=today.day)

    return render(req, 'main/analitycs.html', locals())
