# Generated by Django 2.2.5 on 2019-10-07 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0029_auto_20191007_0219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occupiedauditorium',
            old_name='aud_id',
            new_name='aud',
        ),
        migrations.RenameField(
            model_name='occupiedauditorium',
            old_name='day_id',
            new_name='day',
        ),
        migrations.RenameField(
            model_name='occupiedauditorium',
            old_name='time_id',
            new_name='time',
        ),
    ]