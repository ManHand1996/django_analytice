from django.shortcuts import render,HttpResponse
import uuid
# Create your views here.


def index(request):
    request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()
    request.session['ff'] = 'index'
    return HttpResponse('hello world' + request.session.session_key )