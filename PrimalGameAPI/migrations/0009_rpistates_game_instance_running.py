# Generated by Django 5.0.4 on 2024-05-05 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrimalGameAPI', '0008_rpistates_gp17'),
    ]

    operations = [
        migrations.AddField(
            model_name='rpistates',
            name='game_instance_running',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
