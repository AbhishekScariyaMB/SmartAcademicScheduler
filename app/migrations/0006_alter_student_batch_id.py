# Generated by Django 3.2.9 on 2022-07-07 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_meetingtime_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch_id',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
