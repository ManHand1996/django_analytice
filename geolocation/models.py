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
    同一IP 可能有多个用户访问
    """
    user_agent = models.TextField(max_length=100, default='')
    ip = models.TextField(max_length=100, default='', primary_key=True, verbose_name='IP地址')
    geo_country = models.TextField(max_length=100, default='' , verbose_name='国家')
    geo_subdivision = models.TextField(max_length=100, default='', verbose_name='省份')
    geo_city = models.TextField(max_length=100, default='', verbose_name='城市')
    longtitude = models.DecimalField(max_digits=15, default=0, decimal_places=6, verbose_name='经度')
    latitude = models.DecimalField(max_digits=15, default=0,  decimal_places=6, verbose_name='纬度')
    visitor = models.ForeignKey(to='SiteVisitor', related_name='geo_visitor', on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.geo_country + self.geo_subdivision + self.geo_city


class VisitRouter(models.Model):
    """
    记录用户访问路径
    """
    path = models.TextField(max_length=500)
    visit_date = models.DateTimeField(default=timezone.now())
    visitor = models.ForeignKey(to='SiteVisitor', related_name='router_visitor', on_delete=models.CASCADE, blank=True,null=True)

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
    # location_info = models.ForeignKey(to='Geolocation', related_name='geolocation', on_delete=models.CASCADE)
    #                                   verbose_name='detail info')
    # visit_path = models.ManyToManyField(VisitRouter, related_name='visitrouter')


