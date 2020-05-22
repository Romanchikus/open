from django.shortcuts import render
from . import models, forms
from django.shortcuts import get_object_or_404
from guardian.mixins import PermissionRequiredMixin
from django.views.generic import (
    UpdateView,
    DetailView,
    CreateView,
    View,
    DeleteView,
    ListView,
)
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, QueryDict, Http404
from django.views.generic.detail import SingleObjectMixin

class ShowHandoutView(DetailView):
    model = models.Handout
    template_name = 'enrollments/handout.html'

class ListHandoutsView(ListView):
    model = models.Handout
    template_name = 'enrollments/list_handouts.html'

    def get_queryset(self):
        # user = self.request.user.profile
        course = models.Course.objects.get(slug=self.kwargs.get('slug'))
        object_list = self.model.objects.filter(course=course).order_by('section')

        return object_list

    def get_context_data(self, **kwargs):
       context = super(ListHandoutsView, self).get_context_data(**kwargs)
       context['course'] = models.Course.objects.get(slug=self.kwargs.get('slug'))
       return context

class UpdateHandoutView(UpdateView):
    model = models.Handout
    template_name = 'enrollments/handout.html'
    fields = '__all__'
    # success_url = reverse_lazy("enrollments:list_handouts")

    def get_success_url(self):
        course = models.Course.objects.get(handout__pk=self.kwargs.get('pk'))
        print(course)
        return reverse('enrollments:list_handouts', kwargs={'slug': course.slug})

class DeleteHandoutView(DeleteView):
    model = models.Handout

    def get_success_url(self):
        course = models.Course.objects.get(handout__pk=self.kwargs.get('pk'))
        print(course)
        return reverse('enrollments:list_handouts', kwargs={'slug': course.slug})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CreateHandoutView(CreateView):
    model = models.Handout
    form_class = forms.HandoutForm
    template_name = 'enrollments/handout.html'
    # success_url =  reverse_lazy('courses:detail')

    def form_valid(self, form):
        form = form.save(commit=False)
        form.course = get_object_or_404(models.Course, slug=self.kwargs.get('slug'))
        print(form.file)
        form.save()
        return super(CreateHandoutView, self).form_valid(form)

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs.get('slug')})

import os
from django.conf import settings

class FileDownloadView(View):
    # Set FILE_STORAGE_PATH value in settings.py
    folder_path = settings.MEDIA_ROOT
    # Here set the name of the file with extension
    file_name = ''
    # Set the content type value
    content_type_value = 'text/plain'

    def get(self, request, pk):
        handout = get_object_or_404(models.Handout, pk=pk)
        self.file_name = str(handout.file)
        print(self.file_name)
        file_path = os.path.join(self.folder_path, self.file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(),
                    content_type=self.content_type_value
                )
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
        else:
            raise Http404


class CreateEnrollmentView(View):

    def post(self, request):
        post = QueryDict(request.body)
        print(post.get("course"))
        student = self.request.user.profile  
        course = post.get("course")
        course = get_object_or_404(models.Course, slug=course)
        if not models.Enrollment.objects.filter(student=student, course=course).exists():
            model = models.Enrollment.objects.get_or_create(student=student, course=course, is_active=None)
        return HttpResponse()

    def put(self, request):
        put = QueryDict(request.body)
        print('PUT!',put.get("enrol_slug"))
        enrollment = get_object_or_404(models.Enrollment, slug=put.get("enrol_slug"))
        action = put.get("action")
        if action:
            enrollment.is_active=True
        else:
            enrollment.is_active=False
        enrollment.save()
        print(enrollment.is_active)
        return HttpResponse()

              
        

class ListEnrollmentView(ListView):
    model = models.Enrollment
    template_name = 'enrollments/list_enrollments.html'

    def get_queryset(self):
        
        user = self.request.user.profile
        object_list = self.model.objects.filter(is_active = None)
        print(object_list)
        object_list = object_list.filter(course__professor=user)
        print(object_list)

        return object_list