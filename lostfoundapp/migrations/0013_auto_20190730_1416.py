# Generated by Django 2.1.7 on 2019-07-30 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lostfoundapp', '0012_remove_matchedrecord_match_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='founder',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lostfoundapp.Profile'),
        ),
        migrations.AlterField(
            model_name='loser',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lostfoundapp.Profile'),
        ),
    ]
