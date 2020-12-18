# Generated by Django 3.1.4 on 2020-12-18 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('print_edition', '0001_initial'),
        ('subscription', '0003_auto_20201218_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='print_edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', related_query_name='subscriptions_query', to='print_edition.printedition'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
