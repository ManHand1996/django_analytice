# -*-coding:utf-8-*-
from .spooler import save_location_info
import uuid
import datetime
from pytz import timezone
from django.conf import settings
from django.urls import resolve


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


