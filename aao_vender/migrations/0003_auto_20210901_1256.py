# Generated by Django 3.1.3 on 2021-09-01 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aao_vender', '0002_vender_details_vd_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='vender_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('vender_name', models.CharField(default=None, max_length=255)),
                ('address_line1', models.CharField(default=None, max_length=255)),
                ('address_line2', models.CharField(default=None, max_length=255)),
                ('address_line3', models.CharField(default=None, max_length=255)),
                ('pincode', models.CharField(default=None, max_length=255)),
                ('city', models.CharField(default=None, max_length=255)),
                ('district', models.CharField(default=None, max_length=255)),
                ('state', models.CharField(default=None, max_length=255)),
                ('country', models.CharField(default=None, max_length=255)),
                ('vender_manager_name', models.CharField(default=None, max_length=255)),
                ('vender_manager_contact_number', models.CharField(default=None, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified_on', models.DateTimeField(auto_now=True)),
                ('last_modified_by', models.CharField(default=None, max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Vender_Details',
        ),
    ]