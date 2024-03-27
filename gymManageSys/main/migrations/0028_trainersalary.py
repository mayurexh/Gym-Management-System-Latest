# Generated by Django 5.0.1 on 2024-03-26 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_trainer_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.IntegerField()),
                ('amt_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.trainer')),
            ],
            options={
                'verbose_name_plural': 'Trainer Salary',
            },
        ),
    ]
