from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path != '/login/' and not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        return response
