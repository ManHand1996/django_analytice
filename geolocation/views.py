import itertools
from django.shortcuts import render,HttpResponse


from pyecharts.globals import ChartType, SymbolType,ThemeType

from pyecharts import options as opts

from pyecharts.charts import Line, Map,Bar
from geolocation.models import SiteVisitor,VisitRouter,Geolocation
import datetime, pytz
from django.db.models import Count
from django.conf import settings
# Create your views here.

init_opt1 = opts.InitOpts(width="100%",height="800px", theme=ThemeType.CHALK)


def user_access_charts(request):

    """
    折线图： 显示近七天访客访问次数
    :param request:
    :return:
    """
    # SQLite 查询日期设置 settings.USE_TZ = False, 查询的时间也不要设置时区，默认使用系统时间，这样查询才正确
    dnow = datetime.datetime.now()
    start_date = dnow - datetime.timedelta(days=7)
    end_date = dnow

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
            .add_xaxis(axis_x)
            .add_yaxis('访问次数', axis_y)
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