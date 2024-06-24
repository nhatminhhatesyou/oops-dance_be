# Generated by Django 5.0.6 on 2024-06-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0048_booking_full_payment_booking_real_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in_progress', 'In Progress'), ('waiting', 'Waiting'), ('cancelled', 'Cancelled')], max_length=20, verbose_name='Status'),
        ),
    ]