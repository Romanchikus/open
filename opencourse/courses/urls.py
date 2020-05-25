from django.urls import path, include
from . import views

app_name = "courses"
urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("list/", views.CourseListView.as_view(), name="list"),
    path("<slug:slug>/detail/", views.CourseDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", views.CourseEditView.as_view(), name="edit"),
    path("<slug:slug>/delete/", views.CourseDeleteView.as_view(), name="delete"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path(
        "search-results/",
        views.CourseSearchResultsView.as_view(),
        name="search_results",
    ),
]
