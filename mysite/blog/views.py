from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Project, Topic, SubTopic
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ProjectForm, TopicForm, SubtopicForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


# from django.contrib.auth.forms import User
# from django.views.decorators.csrf import csrf_protect

def index(request):
    num_projects = Project.objects.filter(status__exact='f').count()
    num_topics = Topic.objects.all().count()
    num_subtopics = SubTopic.objects.all().count()

    context = {
        'num_projects': num_projects,
        'num_topics': num_topics,
        'num_subtopics': num_subtopics,
    }
    return render(request, 'index.html', context=context)


def projects_view(request):
    paginator = Paginator(Project.objects.all(), 8)
    page_number = request.GET.get('page')
    paged_projects = paginator.get_page(page_number)
    projects = paged_projects
    context = {
        'projects': projects,
    }
    return render(request, "projects.html", context=context)


def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    return render(request, 'project.html', context=context)


def search(request):
    query = request.GET.get('query')
    topic_results = Topic.objects.filter(
        Q(topic_name__icontains=query) |
        Q(about__icontains=query)
     )
    subtopic_results = SubTopic.objects.filter(
        Q(sub_topic_name__icontains=query) |
        Q(summary__icontains=query)
    )
    project_results = Project.objects.filter(
        Q(title__icontains=query) |
        Q(short_summary__icontains=query) |
        Q(started__icontains=query) |
        Q(finished__icontains=query) |
        Q(description__icontains=query) |
        Q(by__icontains=query) |
        Q(by_who__icontains=query) |
        Q(status__iexact=query)
    )
    context = {
        'topics': topic_results,
        'subtopics': subtopic_results,
        'projects': project_results,
        'query': query,
    }
    return render(request, 'search.html', context)


class TopicsListView(generic.ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 6


class TopicsDetailView(generic.DetailView):
    model = Topic
    context_object_name = 'topic'
    template_name = 'topic.html'


class SubTopicListview(generic.ListView):
    model = SubTopic
    context_object_name = 'subtopics'
    template_name = 'subtopics.html'


class SubTopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = SubTopic
    context_object_name = 'subtopic'
    template_name = 'subtopic.html'


# @csrf_protect
# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, f'Vartotojo vardas {username} uzimtas')
#                 return redirect('register')
#             else:
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request, f'Toks emeilas {email} uzimtas')
#                     return redirect('register')
#                 else:
#                     User.objects.create_user(username=username, email=email, password=password)
#                     messages.info(request, f'Vartotojas {username} uzregistruotas !')
#                     return redirect('login')
#         else:
#             messages.error(request, 'Slaptazodziai nesutampa')
#             return redirect('register')
#
#     else:
#         return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context=context)


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topics_form.html'
    success_url = '/blog/topics/'

    def test_func(self):
        return self.request.user.is_superuser


class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Topic
    template_name = 'topics_form.html'
    form_class = TopicForm
    success_url = '/blog/topics/'

    def test_func(self):
        return self.request.user.is_superuser


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Topic
    success_url = '/blog/topics/'
    template_name = 'topics_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class SubTopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = SubTopic
    template_name = 'subtopics_form.html'
    form_class = SubtopicForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('topic', kwargs={'pk': self.kwargs['topic_id']})

    def form_valid(self, form):
        form.instance.topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        return super().form_valid(form)


class SubTopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = SubTopic
    template_name = 'subtopics_form.html'
    form_class = SubtopicForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('topic', kwargs={'pk': self.kwargs['topic_id']})

    def form_valid(self, form):
        form.instance.subtopic = SubTopic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class SubTopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = SubTopic
    template_name = 'subtopics_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('topic', kwargs={'pk': self.kwargs['topic_id']})


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Project
    template_name = 'projects_form.html'
    form_class = ProjectForm
    success_url = '/blog/projects/'

    def test_func(self):
        return self.request.user.is_superuser


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Project
    template_name = 'projects_form.html'
    form_class = ProjectForm
    success_url = '/blog/projects/'

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Project
    success_url = '/blog/projects/'
    template_name = 'projects_delete.html'

    def test_func(self):
        return self.request.user.is_superuser
