# Generated by Django 5.0.6 on 2024-05-18 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0006_alter_classschedule_class_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassScheduleLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oopsdance.class', verbose_name='Lớp học')),
                ('schedule_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oopsdance.classschedule', verbose_name='Lịch dạy')),
            ],
            options={
                'verbose_name': 'Liên kết Lớp học và Lịch dạy',
                'unique_together': {('class_id', 'schedule_id')},
            },
        ),
        migrations.AddField(
            model_name='class',
            name='schedules',
            field=models.ManyToManyField(through='oopsdance.ClassScheduleLink', to='oopsdance.classschedule', verbose_name='Lịch dạy'),
        ),
    ]
