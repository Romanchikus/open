from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EnrollmentsConfig(AppConfig):
    name = 'opencourse.enrollments'
    verbose_name = _("Enrollments")
