# Generated by Django 2.1.7 on 2019-07-23 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostfoundapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='device_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
