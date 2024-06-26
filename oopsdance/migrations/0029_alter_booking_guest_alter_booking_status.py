# Generated by Django 5.0.6 on 2024-05-23 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopsdance', '0028_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Khách hàng'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='oopsdance.bookingstatus', verbose_name='Trạng thái đặt chỗ'),
        ),
    ]
