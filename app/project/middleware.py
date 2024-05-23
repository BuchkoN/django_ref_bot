from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            translation.activate(request.user.language)
