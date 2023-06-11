from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path("projects/", views.projects_view, name="projects"),
    path('projects/new>', views.ProjectCreateView.as_view(), name="project_new"),
    path("projects/<int:project_id>", views.project_view, name="project"),
    path("projects/<int:pk>/delete", views.ProjectDeleteView.as_view(), name="projects_delete"),
    path("projects/<int:pk>/update", views.ProjectUpdateView.as_view(), name="projects_update"),
    path("topics/", views.TopicsListView.as_view(), name="topics"),
    path("topics/new", views.TopicCreateView.as_view(), name="topics_new"),
    path("topics/<int:pk>", views.TopicsDetailView.as_view(), name="topic"),
    path("topics/<int:pk>/update", views.TopicUpdateView.as_view(), name="topic_update"),
    path("topics/<int:pk>/delete", views.TopicDeleteView.as_view(), name="topic_delete"),
    path("topics/<int:topic_id>/new_subtopic", views.SubTopicCreateView.as_view(), name="subtopics_new"),
    path("topics/<int:topic_id>/subtopics/<int:pk>", views.SubTopicDetailView.as_view(), name="subtopic"),
    path("topics/<int:topic_id>/subtopics/<int:pk>/update", views.SubTopicUpdateView.as_view(), name="subtopic_update"),
    path("topics/<int:topic_id>/subtopics/<int:pk>/delete", views.SubTopicDeleteView.as_view(), name="subtopic_delete"),
]
