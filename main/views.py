from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from .forms import PersonForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from project.settings import APP_NAME


@login_required
def home(req):
    app_name = APP_NAME
    return render(req, 'main/home.html', locals())


class LoginHandler(View):
    template_name = 'main/login.html'

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        app_name = APP_NAME
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):

        form = PersonForm(request.POST)
        if form.is_valid():
            user = form.get_or_create_user()
            login(request, user)
            return HttpResponse()
        return HttpResponse(form.errors, status=400)


def logout_handler(request):
    logout(request)
    return redirect(reverse('main:LoginHandler'))
