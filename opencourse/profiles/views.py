from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    RedirectView,
    ListView,
    CreateView,
    View,
)
from django.contrib.auth import get_user_model
from django.views.generic.detail import SingleObjectMixin

from opencourse.profiles import forms, models
from opencourse.courses.models import Course

User = get_user_model()


class ProfessorDetailView(ListView):
    model = Course
    template_name = "profiles/professor_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        professor = models.Professor.objects.filter(user_id=pk).first()
        kwargs["professor"] = professor
        kwargs["review_form"] = forms.ReviewForm()
        kwargs["reviews"] = professor.review_set.order_by("-id")[:10]
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = self.model.objects.filter(professor=pk)
        return queryset


class ProfileUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    formset_class = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = self.formset_class(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["formset"] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ProfessorUpdateView(ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("courses:list")
    formset_class = forms.ProfessorFormSet


class StudentUpdateView(ProfileUpdateView):
    template_name = "profiles/profile.html"
    success_url = reverse_lazy("courses:search")
    formset_class = forms.StudentFormSet


class ProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            return reverse_lazy("profiles:professor")
        elif hasattr(self.request.user, "student"):
            return reverse_lazy("profiles:student")
        return super().get_redirect_url(*args, **kwargs)


class DispatchLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request.user, "professor"):
            if self.request.user.professor.course_set.exists():
                return reverse_lazy("courses:list")
            else:
                return reverse_lazy("courses:create")
        return reverse_lazy("courses:search")


class ReviewCreateView(CreateView):
    form_class = forms.ReviewForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("profiles:professor_detail", args=[pk])

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        pk = self.kwargs["pk"]
        professor = models.Professor.objects.filter(user_id=pk).first()
        form.instance.professor = professor
        return super().form_valid(form)


class ContactRequestView(SingleObjectMixin, View):
    model = models.Professor

    def post(self, *args, **kwargs):
        professor = self.get_object()
        professor.contacts_requests += 1
        professor.save()
        return HttpResponse()
