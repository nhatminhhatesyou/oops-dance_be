# Generated by Django 5.0.6 on 2024-06-06 15:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0040_class_class_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
