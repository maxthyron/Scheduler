# Generated by Django 2.2.5 on 2019-10-07 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0031_auto_20191007_0237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservedauditorium',
            old_name='aud',
            new_name='auditorium',
        ),
    ]
