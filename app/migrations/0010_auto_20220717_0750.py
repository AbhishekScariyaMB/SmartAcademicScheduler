# Generated by Django 3.2.9 on 2022-07-17 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20220711_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='attstring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=25)),
                ('day', models.CharField(max_length=50)),
                ('def_string', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'attstring',
            },
        ),
        migrations.RenameField(
            model_name='attendence',
            old_name='Att_str',
            new_name='att_str',
        ),
    ]
