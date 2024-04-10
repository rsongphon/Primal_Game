# Generated by Django 5.0.4 on 2024-04-10 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LoginLogoutHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_hist', models.DateTimeField()),
                ('logout_hist', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Primals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RPiBoards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('ssid', models.CharField(max_length=32)),
                ('ssid_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GameInstances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PrimalGameAPI.games')),
                ('login_hist', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='PrimalGameAPI.loginlogouthist')),
                ('primal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primal', to='PrimalGameAPI.primals')),
                ('rpiboard', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rpiboard', to='PrimalGameAPI.rpiboards')),
            ],
        ),
        migrations.CreateModel(
            name='RPiStates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_occupied', models.BooleanField(default=False)),
                ('rpiboard', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PrimalGameAPI.rpiboards')),
            ],
        ),
    ]
