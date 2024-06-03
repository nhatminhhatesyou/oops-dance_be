# Generated by Django 5.0.6 on 2024-06-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0034_alter_attendance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='bank_transfer',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chuyển khoản'),
        ),
        migrations.AddField(
            model_name='booking',
            name='cash',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tiền mặt'),
        ),
        migrations.AddField(
            model_name='booking',
            name='deposited',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tiền đặt cọc'),
        ),
        migrations.AddField(
            model_name='booking',
            name='details',
            field=models.TextField(blank=True, null=True, verbose_name='Chi tiết'),
        ),
    ]
