# Generated by Django 3.2.9 on 2022-07-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_attendence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendence',
            old_name='Date',
            new_name='date',
        ),
        migrations.AddField(
            model_name='attendence',
            name='day',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]