# Generated by Django 3.0.5 on 2020-05-25 09:45

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '__first__'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(upload_to='files')),
                ('section', models.CharField(choices=[('PDF', 'PDF'), ('docx', 'docx'), ('Photo', 'Photo')], default='PDF', max_length=15)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'verbose_name': 'Handout',
                'verbose_name_plural': 'Handout',
                'permissions': (('manage_handout', 'Manage handout'),),
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(unique=True)),
                ('is_active', models.NullBooleanField(default=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Student')),
            ],
            options={
                'verbose_name': 'Enrollment',
                'verbose_name_plural': 'Enrollment',
                'permissions': (('manage_enrollment', 'Manage enrollment'),),
            },
        ),
    ]
