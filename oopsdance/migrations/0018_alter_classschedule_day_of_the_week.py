# Generated by Django 5.0.6 on 2024-05-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0017_alter_classschedule_day_of_the_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classschedule',
            name='day_of_the_week',
            field=models.CharField(choices=[('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday'), ('8', 'Sunday')], default='4', max_length=10, verbose_name='Day of the Week'),
        ),
    ]
