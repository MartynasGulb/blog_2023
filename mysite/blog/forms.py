from django import forms
from .models import Profile, Topic, SubTopic, Project
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'short_summary', 'code', 'by', 'by_who', 'status', 'git', 'started', 'finished']
        widgets = {'started': DateInput(), 'finished': DateInput()}


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_name', 'about', 'project']


class SubtopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = ['sub_topic_name', 'summary']
