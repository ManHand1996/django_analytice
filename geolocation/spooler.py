# -*-coding:utf-8-*-

from uwsgidecorators import spool
import geolocation.geotrans as geotrans
# return value :
# -2 OK SPOOL_OK
# -1 retry SPOOL_RETRY
# 0 passed the task SPOOL_IGNORE

@spool
def save_location_info(userinfo):
    geotrans.trans_to_location(userinfo)