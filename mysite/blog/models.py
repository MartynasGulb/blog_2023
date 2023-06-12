from django.db import models
from PIL import Image
from datetime import date
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Topic(models.Model):
    topic_name = models.CharField('Topic', max_length=200, blank=True)
    about = HTMLField('About',  blank=True)
    project = models.ManyToManyField(to='Project', verbose_name='project', blank=True)

    def __str__(self):
        return self.topic_name


class SubTopic(models.Model):
    sub_topic_name = models.CharField('Sub Topic', max_length=200, blank=True)
    summary = HTMLField('Summary', blank=True)
    topic = models.ForeignKey(to='Topic', verbose_name='Topic', on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='subtopics')

    def __str__(self):
        return self.sub_topic_name

    class Meta:
        ordering = ['sub_topic_name']


class Project(models.Model):
    title = models.CharField('Title', max_length=200, default='Project name')
    short_summary = models.TextField(verbose_name="Summary", max_length=1000, default='Short summary')
    started = models.DateField('Started', null=True, blank=True)
    finished = models.DateField('Finished', null=True, blank=True)
    code = HTMLField(verbose_name='Description', max_length=4000, default='', blank=True, null=True)

    CREATED_BY = (
        ('c', 'CodeAcademy'),
        ('m', 'Me'),
        ('ou', 'Outsourced'),
    )

    PROJECT_STATUS = (
        ('f', 'Finished'),
        ('on', 'Ongoing'),
        ('i', 'Idea'),
    )
    by = models.CharField(verbose_name='Idea by', max_length=2, choices=CREATED_BY, blank=True)
    by_who = models.URLField(verbose_name='source', blank=True)
    status = models.CharField(verbose_name='State', max_length=2, choices=PROJECT_STATUS, blank=True, default='i')
    git = models.URLField(verbose_name='link', blank=True, null=True)
    def __str__(self):
        return self.title

    def is_finished(self):
        return self.finished and date.today() > self.finished


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Photo', upload_to='profile_pics', default='profile_pics/default.png')

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
