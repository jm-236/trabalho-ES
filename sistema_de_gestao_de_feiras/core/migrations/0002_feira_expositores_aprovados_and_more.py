# Generated by Django 5.2.3 on 2025-06-29 19:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feira',
            name='expositores_aprovados',
            field=models.ManyToManyField(blank=True, related_name='feiras_aprovadas', to='core.expositor'),
        ),
        migrations.AddField(
            model_name='feira',
            name='expositores_pendentes',
            field=models.ManyToManyField(blank=True, related_name='feiras_pendentes', to='core.expositor'),
        ),
        migrations.AlterField(
            model_name='feira',
            name='organizador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feiras_organizadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
