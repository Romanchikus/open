from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DetailView
from django_filters.views import FilterView

from . import forms, models, filters
from .mixins import FormsetMixin
from opencourse.profiles.forms import ReviewForm
from opencourse.profiles.mixins import ProfessorRequiredMixin


class CourseEditView(ProfessorRequiredMixin, FormsetMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")


class CourseCreateView(ProfessorRequiredMixin, FormsetMixin, CreateView):
    form_class = forms.CourseForm
    formset_class = forms.CourseLocationFormset
    template_name = "courses/edit.html"
    exclude = ["professor"]
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        form.instance.professor = self.request.user.professor
        return super().form_valid(form)


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
        kwargs["reviews"] = self.object.professor.review_set.order_by("-id")[:10]
        return super().get_context_data(**kwargs)


class CourseSearchView(FormView):
    template_name = "courses/search.html"
    form_class = forms.CourseSearchForm
    success_url = reverse_lazy("courses:search")


class CourseSearchResultsView(FilterView):
    filterset_class = filters.CourseFilter
    template_name = "courses/search_results.html"
    paginate_by = 10
