# Generated by Django 5.0.1 on 2024-02-19 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_subplanfeature_subplan_subplanfeature_subplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='max_member',
            field=models.IntegerField(null=True),
        ),
    ]
