import itertools

from django.shortcuts import render,HttpResponse
from django.urls import resolve
from .decorators import makeuserinfo
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader('../geolocation/templates'))
from pyecharts import options as opts
from pyecharts.charts import Line
from .models import SiteVisitor,VisitRouter,Geolocation
# Create your views here.

@makeuserinfo
def index(request):
    # request.session['session_uuid'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'user').__str__()
    # request.session['ff'] = 'index'
    # rq = request.session.get('session_uuid')
    # remote_addr = request.META.get('REMOTE_ADDR').__str__()
    # http_host = request.META.get('HTTP_HOST ').__str__()
    # http_host = request.get_host().__str__()
    # user_agent = request.headers['User-Agent'].__str__()

    return HttpResponse('hello world' )


def articles(request, *args, **kwargs):
    f = resolve(request.path)
    return HttpResponse('fff' + f.route.__str__())


def user_access_charts(request):
    query_set = SiteVisitor.objects.filter(session_uuid__isnull=False).values('last_income_date')
    group_set = itertools.groupby(query_set, lambda d : d.get('last_income_date').strftime('%Y-%m-%d'))
    axis_x = []
    axis_y = []
    for day, this_day in group_set:
        axis_x.append(day)
        axis_y.append(len(list(this_day)))
    axis_y.append(100)
    chart = (
        Line()
            .add_xaxis(axis_x)
            .add_yaxis('access_date', axis_y)
            .set_global_opts(title_opts=opts.TitleOpts(title="用户访问统计", subtitle="每天"))
    )
    return HttpResponse(chart.render_embed())


def geolocation_charts():
    pass


def path_access_charts():
    pass