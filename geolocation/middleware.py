# -*-coding:utf-8-*-
from .spooler import save_location_info
import uuid
import datetime
from pytz import timezone
from django.conf import settings
from django.urls import resolve

class UserinfoMiddelware:
    """
    自定义中间件：获取用户访问信息，并生成uuid记录
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def ismatchurl(self, path):

        if resolve(path) is not None:
                return True
        return False

    def get_addr(self, request):
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

    def __call__(self, request):
        # 加载视图前执行
        if not request.session.get('session_uuid'):
            request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()

        seesion_uuid = request.session.get('session_uuid')
        visit_time = datetime.datetime.now(tz=timezone('Asia/Shanghai'))

        # 指定URL
        if self.ismatchurl(request.path):
            save_location_info.spool({b'ip': bytes(self.get_addr(request), encoding='utf8'),
                                      b'user_agent': bytes(request.headers['User-Agent'].__str__(), encoding='utf8'),
                                      b'path': bytes(request.path, encoding='utf8'),
                                      b'session_uuid': bytes(seesion_uuid, encoding='utf8'),
                                      b'visit_date': bytes(visit_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                           encoding='utf8')
                                      })
        # print('using UserinfoMiddelware')
        response = self.get_response(request)

        # 加载视图后执行
        return response


class MultipleProxyMiddleware:
    """
    获取使用代理的访问原始地址
    """
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
        # print('using MultipleProxyMiddleware')
        return self.get_response(request)


