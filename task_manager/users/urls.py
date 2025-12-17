from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="users_list"),
    path("create/", views.UserFormView.as_view(), name="user_create"),
]
'''
    path("<int:id>/update/", views.ArticleFormUpdateView.as_view(), name="article_update"),
    path("<int:id>/delete/", views.ArticleFormDeleteView.as_view(), name="article_delete"),
    path("<int:id>/", views.ArticleDetailView.as_view(), name="article_detail"),
'''