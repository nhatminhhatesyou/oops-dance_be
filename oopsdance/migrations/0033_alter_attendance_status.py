# Generated by Django 5.0.6 on 2024-06-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0032_alter_attendance_checkin_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in_progress', 'In Progress'), ('canceled', 'Canceled')], max_length=20, verbose_name='Status'),
        ),
    ]