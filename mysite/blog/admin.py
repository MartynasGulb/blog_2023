from django.contrib import admin
from . import models


class SubTopicAdmin(admin.ModelAdmin):
    list_display = ['topic', 'sub_topic_name']


class TopicAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'started', 'by', 'started', 'finished']


admin.site.register(models.SubTopic, SubTopicAdmin)
admin.site.register(models.Topic)
admin.site.register(models.Project, ProjectAdmin)
