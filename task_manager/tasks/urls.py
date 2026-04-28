from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks_list"),
    path("create/", views.TaskCreateView.as_view(), name="tasks_create"),
    path(
        "<int:pk>/update/",
        views.TaskFormUpdateView.as_view(),
        name="tasks_update",
    ),
    path(
        "<int:pk>/delete/", views.TaskDeleteView.as_view(), name="tasks_delete"
    ),
    path("<int:pk>/show/", views.TaskShowView.as_view(), name="tasks_show"),
]
