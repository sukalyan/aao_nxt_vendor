# Generated by Django 3.1.3 on 2021-09-01 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aao_vender', '0006_auto_20210901_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vender_details',
            name='vd_aao_balance',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='vender_details',
            name='vd_aao_user',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
