# Generated by Django 3.2.9 on 2022-02-12 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_teacher_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='qualifiication',
            new_name='qualification',
        ),
    ]
