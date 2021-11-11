# -*-coding:utf-8-*-
from functools import wraps
import uuid
from django.http import Http404
from geolocation.spooler import save_location_info
from django.utils import timezone
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
            return request.META['HTTP_X_FORWARDED_FOR']
        else:
            return request.META.get('REMOTE_ADDR').__str__()

    @wraps(func)
    def wrapfunc(request, *args, **kwargs):
        if not request.session.get('session_uuid'):
            request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()

        seesion_uuid = request.session.session_key
        # visit_time = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        visit_time = timezone.now()
        client_ip = get_addr(request)
        # 指定URL
        if request.method == 'GET':
            save_location_info.spool({b'ip': bytes(client_ip, encoding='utf8'),
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
