# Generated by Django 2.2.2 on 2019-07-07 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20190707_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='schedulesubject',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='schedulesubject',
            name='start_time',
        ),
        migrations.AddField(
            model_name='schedulesubject',
            name='time_id',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.PROTECT, to='schedule.ScheduleTime'),
            preserve_default=False,
        ),
    ]
