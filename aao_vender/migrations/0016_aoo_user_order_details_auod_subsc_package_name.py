# Generated by Django 3.2.7 on 2021-09-23 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aao_vender', '0015_auto_20210920_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='aoo_user_order_details',
            name='auod_subsc_package_name',
            field=models.TextField(default=None, max_length=100),
        ),
    ]
