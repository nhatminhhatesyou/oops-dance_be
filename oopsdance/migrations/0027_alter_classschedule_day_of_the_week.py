# Generated by Django 5.0.6 on 2024-05-21 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0026_class_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classschedule',
            name='day_of_the_week',
            field=models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('0', 'Sunday')], max_length=10, verbose_name='Day of the Week'),
        ),
    ]