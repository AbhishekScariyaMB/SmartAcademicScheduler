# Generated by Django 3.2.9 on 2022-07-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20220719_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='status',
            field=models.CharField(default=1, max_length=10),
        ),
    ]
