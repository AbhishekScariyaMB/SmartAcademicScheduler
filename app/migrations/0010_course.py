# Generated by Django 3.2.9 on 2022-01-20 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_login_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=5)),
                ('code', models.CharField(max_length=10)),
                ('dept_id', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]
