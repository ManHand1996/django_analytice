import datetime

import pytz
from geoip2 import webservice
from django.conf import settings
import IPy
from geolocation.models import VisitRouter, SiteVisitor, Geolocation


def trans_to_location(userinfo):
    """
    get geoinfo with geoip2.webservice online requests
    url： https://maxmind.com
    docs：https://geoip2.readthedocs.io/en/latest/#geoip2.models.City
    :param userinfo: {}
    :return:
    """
    # ipv4 ip address
    ip_addr = userinfo['ip']
    userinfo['city'] = ''
    userinfo['country'] = ''
    userinfo['subdivision'] = ''
    userinfo['longtitude'] = 0
    userinfo['latitude'] = 0
    #userinfo['visit_date'] = datetime.datetime.strptime(userinfo['visit_date'], '%Y-%m-%d %H:%M:%S')
    d_date = datetime.datetime.strptime(userinfo['visit_date'], '%Y-%m-%d %H:%M:%S')
    userinfo['visit_date'] = d_date.replace(tzinfo=pytz.timezone(settings.TIME_ZONE)) if settings.USE_TZ else d_date
    try:
        IPy.IP(ip_addr)
        r = Geolocation.objects.filter(ip=ip_addr)

        if len(r) == 0:
            # get ip info from geolite.info
            with webservice.Client(settings.MAXMIND_ACCOUNT, settings.MAXMIND_LICENSE, host='geolite.info', locales=['zh-CN','en']) as client:
                response = client.city(ip_addr)

                userinfo['city'] = response.city.name
                userinfo['country'] = response.country.name
                userinfo['subdivision'] = response.subdivisions[0].name
                userinfo['longtitude'] = response.location.longtitude
                userinfo['latitude'] = response.location.latitude
        else:
            userinfo['city'] = r[0].city
            userinfo['country'] = r[0].country
            userinfo['subdivision'] = r[0].subdivision
            userinfo['longtitude'] = r[0].longtitube
            userinfo['latitude'] = r[0].latitube

    except Exception as e:
        pass
    save_info(userinfo)
    # save info to database


def save_info(info_dict):
    # 保存到数据库
    """

    :param info_dict: {'ip':'', 'user_agent':'', 'session_uuid':'', 'city':'','country':'','subdivision':''}
    ip地址，浏览器，session_uuid, 城市，国家，省份
    :return:
    """

    # modelA.createobjs
    # modelB.createobjs
    # modelC.createobjs
    # modelA -> modelB, modelC
    ip_addr = info_dict['ip']
    city = info_dict['city']
    country = info_dict['country']
    subdivision = info_dict['subdivision']
    session_uuid = info_dict['session_uuid']
    path = info_dict['path']
    user_agent = info_dict['user_agent']
    visit_date = info_dict['visit_date']
    longtitude = info_dict['longtitude']
    latitude = info_dict['latitude']

    # 多对一关系
    # 指定主键 则根据主键判断对象是否存在：
    # 存在：更新
    # 不存在：插入
    location, created = Geolocation.objects.update_or_create(defaults={'user_agent': user_agent,
                                                                       'geo_country': country,
                                                                       'geo_city': city,
                                                                       'geo_subdivision': subdivision,
                                                                       'longtitude': longtitude,
                                                                       'latitude': latitude
                                                                       },
                                                             ip=ip_addr)

    # update_or_craete(defaults={},*kwargs)
    # defaults={} 更新列
    visitor, created = SiteVisitor.objects.update_or_create(defaults={'last_income_date': visit_date,
                                                                      'location_info':location},
                                                            session_uuid=session_uuid)
    if created:
        router = VisitRouter.objects.create(path=path)
        visitor.visit_path.add(router)
        # visitor.location_info.update(location)
    else:
        visitor.visit_path.update_or_create(defaults={'visit_date': visit_date}, path=path)
        # 判断用户的同一天访问记录是否存在 不存在就添加，存在则更新
        # visitor.update(last_income_date)
        # visitor.visit_path.add() 同一用户同一天访问同一个路径只算一次（同一天只更新一次）



