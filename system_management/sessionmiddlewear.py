from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
class SessionRenewalMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.session.set_expiry(1200)  
