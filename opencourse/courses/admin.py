from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from modeltranslation.admin import TranslationAdmin
from opencourse.courses import models


class CourseInline(admin.TabularInline):
    model = models.CourseLocation


class CourseAdmin(GuardedModelAdmin):
    inlines = [
        CourseInline,
    ]


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Currency)
admin.site.register(models.CourseDuration)
model_objects = (
    models.CourseArea,
    models.City,
    models.CourseLevel,
    models.CourseAge,
    models.CourseLanguage,
    models.CourseLocationType,
)

for m in model_objects:
    admin.site.register(m, type(m.__name__ + "Admin", (admin.ModelAdmin,), {}))
