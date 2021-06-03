from django.contrib import admin
from . import models


admin.site.register(models.Entries)
admin.site.register(models.EntriesStatistics)