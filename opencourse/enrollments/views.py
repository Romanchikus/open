from django.shortcuts import render
from . import models, forms
from django.shortcuts import get_object_or_404
from guardian.mixins import PermissionRequiredMixin
from opencourse.profiles.mixins import ProfessorRequiredMixin, StudentRequiredMixin
from django.views.generic import (
    UpdateView,
    DetailView,
    CreateView,
    View,
    DeleteView,
    ListView,
)
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, QueryDict, Http404, HttpResponseForbidden
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
        try:
           context['is_active'] = models.Enrollment.objects.get(
               course=context['course'], student= self.request.user.student).is_active
        except:
            pass
        return context

class UpdateHandoutView(ProfessorRequiredMixin,UpdateView):
    model = models.Handout
    template_name = 'enrollments/handout.html'
    fields = '__all__'
    # success_url = reverse_lazy("enrollments:list_handouts")

    def get_success_url(self):
        course = models.Course.objects.get(handout__pk=self.kwargs.get('pk'))
        print(course)
        return reverse('enrollments:list_handouts', kwargs={'slug': course.slug})

class DeleteHandoutView(ProfessorRequiredMixin,DeleteView):
    model = models.Handout

    def get_success_url(self):
        course = models.Course.objects.get(handout__pk=self.kwargs.get('pk'))
        print(course)
        return reverse('enrollments:list_handouts', kwargs={'slug': course.slug})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CreateHandoutView(ProfessorRequiredMixin,CreateView):
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
from urllib.parse import quote

class FileDownloadView(View):
    # Set FILE_STORAGE_PATH value in settings.py
    folder_path = settings.MEDIA_ROOT
    # Here set the name of the file with extension
    file_name = ''
    # Set the content type value
    content_type_value = 'text/plain'

    def get(self, request, pk):
        handout = get_object_or_404(models.Handout, pk=pk)
        file_path = os.path.join(self.folder_path, str(handout.file))
        filename=os.path.basename(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                print(os.path.basename(file_path))
                response = HttpResponse(fh.read(), content_type='application/force-download')
                try:
                    filename.encode('ascii')    
                    file_expr = 'filename="{}"'.format(filename)
                except UnicodeEncodeError:
                    file_expr = "filename*=utf-8''{}".format(quote(filename))
                response['Content-Disposition'] = 'attachment; {}'.format(file_expr)
                return response

class CreateEnrollmentView(UpdateView):

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
        print('PUT!',put.get("action")=='True')
        enrollment = get_object_or_404(models.Enrollment, slug=put.get("enrol_slug"))
        action = put.get("action")
        if action=='True':
            enrollment.is_active=True
        else:
            enrollment.is_active=False
        enrollment.save()
        print(enrollment.is_active)
        
        return HttpResponse([1, 2, 3])
        
class StudentListEnrollmentsView(StudentRequiredMixin,ListView):
    model = models.Enrollment
    template_name = 'enrollments/list_enrollments.html'

    def get_queryset(self):
        try:
            object_list = self.model.objects.filter(
                student=self.request.user.student).order_by('is_active')
            return object_list
        except:
            return HttpResponseForbidden()
        
        

class ListEnrollmentView(ProfessorRequiredMixin,ListView):
    model = models.Enrollment
    template_name = 'enrollments/list_enrollments.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        new_context_entry = self.kwargs.get('slug')
        context["course_slug"] = new_context_entry
        return context

    def get_queryset(self):
        try:
            object_list = self.model.objects.filter(
                course__professor=self.request.user.profile).order_by('is_active')
            return object_list
        except:
            return HttpResponseForbidden()
       