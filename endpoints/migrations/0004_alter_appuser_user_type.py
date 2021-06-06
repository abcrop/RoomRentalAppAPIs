# Generated by Django 3.2.4 on 2021-06-06 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0003_alter_appuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='user_type',
            field=models.CharField(choices=[('LL', 'LANDLORD'), ('TN', 'TENANT'), ('AD', 'ADMIN')], max_length=2),
        ),
    ]
