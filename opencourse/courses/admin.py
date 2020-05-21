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

admin.site.register(models.CourseArea, TranslationAdmin)
admin.site.register(models.City, TranslationAdmin)
admin.site.register(models.CourseLevel, TranslationAdmin)
admin.site.register(models.CourseAge, TranslationAdmin)
admin.site.register(models.CourseLanguage, TranslationAdmin)


