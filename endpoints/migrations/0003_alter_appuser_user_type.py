# Generated by Django 3.2.4 on 2021-06-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_auto_20210606_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='user_type',
            field=models.CharField(choices=[('LL', 'LANDLORD'), ('TN', 'TENANT')], max_length=2),
        ),
    ]
