from django.urls import path
from . import views

app_name = "enrollments"
urlpatterns = [

    path("list/", views.ListEnrollmentView.as_view(), name="list"),
    path("post/", views.CreateEnrollmentView.as_view(), name="post"),
    path("<slug:slug>/create_handouts/", views.CreateHandoutView.as_view(), name="create_handouts"),
    path("<slug:slug>/list_handouts/", views.ListHandoutsView.as_view(), name="list_handouts"),
    path("<int:pk>/detail_handouts/", views.ShowHandoutView.as_view(), name="detail_handouts"),
    path("<int:pk>/update_handout/", views.UpdateHandoutView.as_view(), name="update_handout"),
    path("<int:pk>/delete_handout/", views.DeleteHandoutView.as_view(), name="delete_handout"),

]

