# Generated by Django 3.2.9 on 2022-01-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20220121_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='dept_id',
            field=models.IntegerField(),
        ),
    ]
