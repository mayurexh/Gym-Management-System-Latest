# Generated by Django 5.0.1 on 2024-03-26 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_subscription_reg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='facebook',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='instagram',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
