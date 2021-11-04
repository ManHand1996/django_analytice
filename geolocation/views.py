import itertools

from django.shortcuts import render,HttpResponse
from django.urls import resolve
from .decorators import makeuserinfo
from pyecharts.globals import ChartType, SymbolType,ThemeType

from pyecharts import options as opts

from pyecharts.charts import Line, Map,Bar
from .models import SiteVisitor,VisitRouter,Geolocation
import datetime
from django.db.models import Count
# Create your views here.

init_opt1 = opts.InitOpts(width="100%",height="800px", theme=ThemeType.CHALK)

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

    """
    折线图： 显示近七天访客访问次数
    :param request:
    :return:
    """
    dnow = datetime.datetime.now()
    start_date = datetime.datetime(dnow.year,dnow.month,dnow.day,0,0,0) + datetime.timedelta(days=-7)
    end_date = datetime.datetime(dnow.year,dnow.month,dnow.day,0,0,0)
    query_set = SiteVisitor.objects.filter(session_uuid__isnull=False,last_income_date__range=(start_date,end_date))\
        .values('last_income_date')
    group_set = itertools.groupby(query_set, lambda d : d.get('last_income_date').strftime('%Y-%m-%d'))
    axis_x = []
    axis_y = []
    for day, this_day in group_set:
        axis_x.append(day)
        axis_y.append(len(list(this_day)))

    chart = (
        Line(init_opts=init_opt1)
            .add_xaxis('访问次数', axis_x)
            .add_yaxis('日期', axis_y)
            .set_global_opts(title_opts=opts.TitleOpts(title="用户访问统计", subtitle="近7天"),)
    )

    return HttpResponse(chart.render_embed())


def geolocation_charts(request):
    """
    MAP 用户访问位置GEO地图
    :param request:
    :return:
    """
    qs = Geolocation.objects.values('geo_city').annotate(count=Count('geo_city'))
    data = [(obj['geo_city'].replace('市', ''), obj['count']) for obj in qs]
    c = (
        Map(init_opts=init_opt1)

            .add(
            "用户访问位置GEO地图",
            data,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=True),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-中国地图（带城市）"),
            visualmap_opts=opts.VisualMapOpts(textstyle_opts=opts.TextStyleOpts(color="white")),

        )

    )
    return HttpResponse(c.render_embed())


def path_access_charts(request):
    data = VisitRouter.objects.values('path').annotate(count=Count('path'))
    x_data = []
    y_data = []
    for d in data:
        x_data.append(d['path'])
        y_data.append(d['count'])
    c = (
        Bar(init_opts=init_opt1)
        .add_xaxis(x_data)
        .add_yaxis('请求数量', y_data)

        .set_global_opts(title_opts=opts.TitleOpts(title="路径访问统计", subtitle=""))
    )
    return HttpResponse(c.render_embed())