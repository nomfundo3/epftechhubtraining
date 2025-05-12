from django.urls import reverse

def base_url(request):
    protocol = request.scheme
    host = request.get_host()
    host_url = f'{protocol}://{host}'
    return host_url