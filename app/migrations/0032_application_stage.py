# Generated by Django 3.2.9 on 2022-02-22 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20220221_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='stage',
            field=models.CharField(default='1', max_length=15),
        ),
    ]
