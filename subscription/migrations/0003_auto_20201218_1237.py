# Generated by Django 3.1.4 on 2020-12-18 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_auto_20201217_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]