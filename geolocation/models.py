from django.db import models
from django.utils import timezone
# Create your models here.


class Geolocation(models.Model):
    """
    -- 访客详细信息
    浏览器
    IP
    国家
    省份
    城市
    经度
    纬度
    """
    user_agent = models.TextField(max_length=100, default='')
    ip = models.TextField(max_length=100, default='', primary_key=True, verbose_name='IP地址')
    geo_country = models.TextField(max_length=100, default='' , verbose_name='国家')
    geo_subdivision = models.TextField(max_length=100, default='', verbose_name='省份')
    geo_city = models.TextField(max_length=100, default='', verbose_name='城市')
    longtitude = models.DecimalField(max_digits=15, default=0, decimal_places=6, verbose_name='经度')
    latitude = models.DecimalField(max_digits=15, default=0,  decimal_places=6, verbose_name='纬度')


class VisitRouter(models.Model):
    """
    记录用户访问路径
    """
    path = models.TextField(max_length=500)
    visit_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.path

class SiteVisitor(models.Model):
    """
    访客信息：
    访客ID
    第一次访问时间
    最后一次访问时间
    """
    session_uuid = models.TextField(max_length=500, default='', )
    first_income_date = models.DateTimeField(default=timezone.now())
    last_income_date = models.DateTimeField(default=timezone.now())
    location_info = models.ForeignKey(to='Geolocation', related_name='geolocation', on_delete=models.CASCADE,
                                      verbose_name='detail info')
    visit_path = models.ManyToManyField(VisitRouter, related_name='visitrouter', on_delete=models.CASCADE)


