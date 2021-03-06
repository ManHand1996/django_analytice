# Generated by Django 3.2.8 on 2021-11-13 20:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0002_auto_20211113_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitevisitor',
            name='visit_path',
        ),
        migrations.AddField(
            model_name='visitrouter',
            name='visitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='router_visitor', to='geolocation.sitevisitor'),
        ),
        migrations.AlterField(
            model_name='sitevisitor',
            name='first_income_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 15, 5, 210782)),
        ),
        migrations.AlterField(
            model_name='sitevisitor',
            name='last_income_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 15, 5, 210804)),
        ),
        migrations.AlterField(
            model_name='visitrouter',
            name='visit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 20, 15, 5, 210256)),
        ),
    ]
