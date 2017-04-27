# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 17:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplexMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('time_window', models.BigIntegerField()),
                ('frequency', models.BigIntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('measurement_time', models.DateTimeField()),
                ('upload_time', models.DateTimeField()),
                ('complex_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.ComplexMeasurement')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Host')),
            ],
        ),
        migrations.CreateModel(
            name='SensorKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.SensorKind'),
        ),
        migrations.AddField(
            model_name='measurementvalue',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor'),
        ),
        migrations.AddField(
            model_name='complexmeasurement',
            name='sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sensors.Sensor'),
        ),
    ]
