# Generated by Django 5.0.6 on 2024-06-19 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0046_rename_proof_attendance_checkin_proof_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.IntegerField(verbose_name='Giá phòng'),
        ),
    ]