from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from opencourse.courses.models import Course
from opencourse.profiles.models import Student
from django.urls import reverse
from .managers import *

class Enrollment(models.Model):

    slug = AutoSlugField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.NullBooleanField(default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = EnrollmentManager()
    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollment")
        permissions = (("manage_enrollment", _("Manage enrollment")),)

    def __str__(self):
        return 'Enrollment_of_{}'.format(self.student)




class Handout(models.Model):

    SECTION_CHOICES = [
        ('PDF', 'PDF'),
        ('docx', 'docx'),
        ('Photo', 'Photo'),
    ]
    def user_directory_path(self, instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        filename = instance.slug +'.'+ filename.split('.')[1]
        return 'handouts_files/{}/{}'.format(instance.slug, filename)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='files')
    section = models.CharField(
        max_length=15,
        choices=SECTION_CHOICES,
        default='PDF',
    )
    def get_absolute_url(self):
        return reverse('courses:detail', args=[self.course.slug])

    objects = HandoutManager()
    class Meta:
        verbose_name = _("Handout")
        verbose_name_plural = _("Handout")
        permissions = (("manage_handout", _("Manage handout")),)
