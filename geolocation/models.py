from django.db import models
import geoip2
# Create your models here.


class Geolocation(models.Model):
    """
    访客详细信息
    浏览器
    IP
    国家
    省份
    城市
    """
    user_agent = models.TextField(max_length=100, default='')
    ip = models.TextField(max_length=100, default='')
    geo_country = models.TextField(max_length=100, default='')
    # 省份
    geo_subdivision = models.TextField(max_length=100, default='')
    geo_city = models.TextField(max_length=100, default='')


class SiteVisitor(models.Model):
    """
    访客信息：
    访客ID
    第一次访问时间
    最后一次访问时间
    """
    session_id = models.TextField(max_length=500, default='',)
    first_income_date = models.DateTimeField(auto_now=True)
    last_income_date = models.DateTimeField(auto_now=True)
    location_info = models.ForeignKey(to='Geolocation', related_name='geolocation', on_delete=models.CASCADE,
                                      verbose_name='detail info')
    visit_path = models.ForeignKey(to='VisitRouter', related_name='visitrouter', on_delete=models.CASCADE)


class VisitRouter(models.Model):
    """
    记录用户访问路径
    """
    path = models.TextField(max_length=500)
    visit_date = models.DateTimeField(auto_now=True)