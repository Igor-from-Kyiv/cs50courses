from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entries/<str:entry_title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new"),
    path("edit/<str:entry_title>", views.edit_entry, name="edit"),
    path("random", views.random_entry, name="random"),
]

