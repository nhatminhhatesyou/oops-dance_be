# Generated by Django 5.0.6 on 2024-05-16 05:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0002_remove_user_avatar_url_remove_user_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=255, verbose_name='Tên lớp')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Giá')),
                ('instructor', models.ForeignKey(limit_choices_to={'role': 'instructor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Giáo viên')),
            ],
        ),
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Thời gian bắt đầu')),
                ('end_datetime', models.DateTimeField(verbose_name='Thời gian kết thúc')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oopsdance.class', verbose_name='Lớp học')),
            ],
        ),
    ]