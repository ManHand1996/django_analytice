# -*-coding:utf-8-*-
from functools import wraps
from .spooler import save_location_info
import uuid
import datetime
from django.utils import timezone
from django.http import Http404
from django.conf import settings
from django.urls import resolve
from django.views.decorators.http import require_http_methods


def makeuserinfo(func):
    """
       get user request info
       :param func:
       :return:
       """
    def get_addr(request):
        FORWARDED_FOR_FIELDS = [
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_FORWARDED_HOST',
            'HTTP_X_FORWARDED_SERVER',
        ]
        remote_tag = list(set(FORWARDED_FOR_FIELDS).intersection(request.META))
        if remote_tag.__len__() > 0:
            return request.get_host().__str__()
        else:
            return request.META.get('REMOTE_ADDR').__str__()

    @wraps(func)
    def wrapfunc(request, *args, **kwargs):
        if not request.session.get('session_uuid'):
            request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()

        seesion_uuid = request.session.get('session_uuid')
        visit_time = datetime.datetime.now()

        # 指定URL
        if request.method == 'GET':
            save_location_info.spool({b'ip': bytes(get_addr(request), encoding='utf8'),
                                      b'user_agent': bytes(request.headers['User-Agent'].__str__(),
                                                           encoding='utf8'),
                                      b'path': bytes(request.path, encoding='utf8'),
                                      b'session_uuid': bytes(seesion_uuid, encoding='utf8'),
                                      b'visit_date': bytes(visit_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                           encoding='utf8')
                                      })
            return func(request, *args, **kwargs)
        raise Http404('ONLY GET')
    return wrapfunc
