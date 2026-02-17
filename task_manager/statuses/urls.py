from django.urls import path
from . import views

urlpatterns = [
    path("", views.StatusListView.as_view(), name="statuses_list"),
    path("create/", views.StatusCreateView.as_view(), name="statuses_create"),
    path("<int:pk>/update/", views.StatusFormUpdateView.as_view(), name="statuses_update"),
    path("<int:pk>/delete/", views.StatusDeleteView.as_view(), name="statuses_delete"),
]