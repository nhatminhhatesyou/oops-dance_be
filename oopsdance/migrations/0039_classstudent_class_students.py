# Generated by Django 5.0.6 on 2024-06-05 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0038_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('class_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oopsdance.class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(limit_choices_to={'role': 'guest'}, related_name='student_classes', through='oopsdance.ClassStudent', to=settings.AUTH_USER_MODEL, verbose_name='Học viên'),
        ),
    ]
