from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    UpdateView,
    DetailView,
    DeleteView,
)

from django_filters.views import FilterView
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm
from opencourse.enrollments.models import Enrollment
from . import forms, models, filters
from .mixins import FormsetMixin
from opencourse.profiles.forms import ReviewForm
from opencourse.profiles.mixins import ProfessorRequiredMixin

REVIEW_COUNT = 10


class CoursePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "courses.manage_course"
    return_403 = True


class CourseEditView(CoursePermissionRequiredMixin, FormsetMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")
    permission_required = "courses.manage_course"
    return_403 = True

class CourseCreateView(ProfessorRequiredMixin, FormsetMixin, CreateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.professor = self.request.user.professor
            response = super().form_valid(form)
            course = self.object
            assign_perm("manage_course", course.professor.user, course)
            return response


class CourseListView(ProfessorRequiredMixin, ListView):
    template_name = "courses/list.html"
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        professor = self.request.user.professor
        return models.Course.objects.created_by(professor=professor)


class CourseDetailView(DetailView):
    model = models.Course
    template_name = "courses/detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["review_form"] = ReviewForm()
        kwargs["professor"] = self.object.professor
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[
            :REVIEW_COUNT
        ]
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[:10]
        try:
            kwargs["has_enroll"] = Enrollment.objects.filter(student=self.request.user.student, course=self.object).exists()
            if kwargs["has_enroll"]:
                kwargs["active_enroll"] = Enrollment.objects.get(student=self.request.user.student, course=self.object).is_active
        except:
            pass
        return super().get_context_data(**kwargs)


class CourseDeleteView(CoursePermissionRequiredMixin, DeleteView):
    model = models.Course
    success_url = reverse_lazy("courses:list")
    template_name = "courses/confirm_delete.html"


class CourseSearchView(FormView):
    template_name = "courses/search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    filterset_class = filters.CourseFilter
    template_name = "courses/search_results.html"
    paginate_by = 10
