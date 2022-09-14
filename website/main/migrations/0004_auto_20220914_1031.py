# Generated by Django 3.2.15 on 2022-09-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220914_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answered',
        ),
        migrations.AddField(
            model_name='question',
            name='is_answered',
            field=models.BooleanField(default=False, verbose_name='Answered'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_marked',
            field=models.BooleanField(default=False, verbose_name='Marked'),
        ),
    ]
