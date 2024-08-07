# Generated by Django 5.0.6 on 2024-05-18 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0007_classschedulelink_class_schedules'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='schedules',
        ),
        migrations.AlterField(
            model_name='classschedule',
            name='class_id',
            field=models.ForeignKey(db_column='class_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='oopsdance.class', verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='classschedule',
            name='day_of_the_week',
            field=models.CharField(choices=[('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday'), ('CN', 'Sunday')], default='2', max_length=10, verbose_name='Day of the Week'),
        ),
        migrations.DeleteModel(
            name='ClassScheduleLink',
        ),
    ]
