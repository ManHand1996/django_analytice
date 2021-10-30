from django.shortcuts import render,HttpResponse
from django.urls import resolve
# Create your views here.


def index(request):
    # request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()
    # request.session['ff'] = 'index'
    # rq = request.session.get('session_uuid')
    # remote_addr = request.META.get('REMOTE_ADDR').__str__()
    # http_host = request.META.get('HTTP_HOST ').__str__()
    # http_host = request.get_host().__str__()
    # user_agent = request.headers['User-Agent'].__str__()
    f = resolve('/articles/2021/')
    return HttpResponse('hello world' + f.route.__str__())


def articles(request, *args, **kwargs):
    f = resolve(request.path)
    return HttpResponse('fff' + f.route.__str__())