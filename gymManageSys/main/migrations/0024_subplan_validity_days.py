# Generated by Django 5.0.1 on 2024-03-26 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_rename_subscriber_assignsubscriber_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='validity_days',
            field=models.IntegerField(null=True),
        ),
    ]
