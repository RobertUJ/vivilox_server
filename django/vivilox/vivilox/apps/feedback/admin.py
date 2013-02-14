from django.contrib import admin
from django.contrib.admin import ModelAdmin

from vivilox.apps.feedback.models import feedbacks

admin.site.register(feedbacks)
