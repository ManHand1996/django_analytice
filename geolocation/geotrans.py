from geoip2 import webservice
from django.conf import settings


def trans_to_location(ip_addr):
    """
    get geoinfo with geoip2.webservice online requests
    url： https://maxmind.com
    docs：https://geoip2.readthedocs.io/en/latest/#geoip2.models.City
    :param ip_addr: visitor ip
    :param account_id: Your MaxMind account ID.
    :param license_key: Your MaxMind license key.
    :return:
    """
    # get ip info from geolite.info
    with webservice.AsyncClient(settings.MAXMIND_ACCOUNT, settings.MAXMIND_LICENSE, host='geolite.info', locales=['zh-CN','en']) as client:
        response = client.city(ip_addr)

        print(response.city.name)
        print(response.country.name)
        print(response.subdivisions[0].name)

    # save info to database

