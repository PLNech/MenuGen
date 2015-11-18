# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20151111_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='unlikes',
            new_name='unlikes_ingredient',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='bad_profiles',
            field=models.ManyToManyField(to='menus.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='activity',
            field=models.CharField(default=2, blank=True, max_length=16, null=True, choices=[('low', 'Sédentaire'), ('light', 'Légère'), ('moderate', 'Modérée'), ('active', 'Régulière'), ('extreme', 'Intense')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.FloatField(default=170),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(default='man', max_length=16, choices=[('man', 'Homme'), ('woman', 'Femme')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(default=75),
            preserve_default=True,
        ),
    ]
