# Generated by Django 3.2.9 on 2022-07-20 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_submission_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='student_id',
            field=models.BigIntegerField(),
        ),
    ]