from django.contrib import admin

from .models import *

admin.site.register(SensorKind)
admin.site.register(Sensor)
admin.site.register(ComplexMeasurement)
admin.site.register(Host)
admin.site.register(MeasurementValue)
