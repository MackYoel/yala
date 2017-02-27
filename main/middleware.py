from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.contrib.auth import login


class DevMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated():
            try:
                user = User.objects.get(pk=13)
                login(request, user)
            except User.DoesNotExist:
                pass
