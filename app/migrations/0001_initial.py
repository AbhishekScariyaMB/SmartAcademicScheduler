# Generated by Django 3.2.9 on 2022-01-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('utype_id', models.CharField(max_length=15)),
                ('status', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'login',
            },
        ),
        migrations.CreateModel(
            name='utype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'utype',
            },
        ),
    ]
