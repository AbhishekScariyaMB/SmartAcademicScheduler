# Generated by Django 3.2.9 on 2022-02-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='ug',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]
