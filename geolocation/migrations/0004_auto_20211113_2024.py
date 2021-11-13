# Generated by Django 3.2.8 on 2021-11-13 20:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0003_auto_20211113_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitevisitor',
            name='location_info',
        ),
        migrations.AddField(
            model_name='geolocation',
            name='visitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='geo_visitor', to='geolocation.sitevisitor'),
        ),
        migrations.AlterField(
            model_name='sitevisitor',
            name='first_income_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 24, 15, 503176)),
        ),
        migrations.AlterField(
            model_name='sitevisitor',
            name='last_income_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 24, 15, 503193)),
        ),
        migrations.AlterField(
            model_name='visitrouter',
            name='visit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 24, 15, 502746)),
        ),
        migrations.AlterField(
            model_name='visitrouter',
            name='visitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='router_visitor', to='geolocation.sitevisitor'),
        ),
    ]
