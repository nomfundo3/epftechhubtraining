from django.shortcuts import redirect
from django.urls import reverse

class restrict_access_middleware:
    def __init__(self,get_response):
         self.get_response = get_response


    def __call__(self,request):
        token = request.session.get('token')
        response = self.get_response(request)
        url = request.path
        if url in reverse('login_view'):
             return response
        if '_api' in url:
             return response
        if not token:
              return redirect('login_view')  
        return response
        
        