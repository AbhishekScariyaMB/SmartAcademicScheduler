# Generated by Django 3.2.9 on 2022-01-21 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_course_dept_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='utype_id',
            field=models.BigIntegerField(),
        ),
    ]
