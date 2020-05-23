from django.db import models


class EnrollmentManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, student):
        return self.filter(student=student)

class HandoutManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)
