# Generated by Django 2.1.7 on 2019-08-30 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostfoundapp', '0019_auto_20190828_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('im1', models.ImageField(upload_to='')),
                ('im2', models.ImageField(upload_to='')),
            ],
        ),
    ]
