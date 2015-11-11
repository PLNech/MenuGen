# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='bad_diets',
            field=models.ManyToManyField(to='menus.Diet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingredientfamily',
            name='bad_diets',
            field=models.ManyToManyField(to='menus.Diet'),
            preserve_default=True,
        ),
    ]
