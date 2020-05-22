# Generated by Django 3.0.5 on 2020-05-21 08:44

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0002_enrollment_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='is_active',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True),
        ),
    ]
