# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('friends', models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('picture', stdimage.models.StdImageField(upload_to='media/images/diet', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IngredientFamily',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('father', models.ForeignKey(to='menus.IngredientFamily', default=None, null=True)),
                ('ingredients', models.ManyToManyField(to='menus.Ingredient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IngredientNutriment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('ingredient', models.ForeignKey(to='menus.Ingredient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('day', models.IntegerField()),
                ('type', models.IntegerField(choices=[(0, 'midi'), (1, 'soir')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('price', models.IntegerField(choices=[(0, 'Bon marché'), (1, 'Moyen'), (2, 'Assez cher')])),
                ('difficulty', models.IntegerField(choices=[(0, 'Très facile'), (1, 'Facile'), (2, 'Moyenne'), (3, 'Difficile')])),
                ('nb_people', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nutriment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('unit_per_100g', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(default='Sans nom', max_length=64)),
                ('birthday', models.DateField(null=True, auto_now_add=True)),
                ('weight', models.IntegerField(default=75, null=True, blank=True)),
                ('height', models.FloatField(default=1.7, null=True, blank=True)),
                ('sex', models.CharField(choices=[('man', 'Homme'), ('woman', 'Femme')], default='man', max_length=16, null=True, blank=True)),
                ('activity', models.CharField(choices=[(0, 'Sédentaire'), (1, 'Légère'), (2, 'Modérée'), (3, 'Régulière'), (4, 'Intense')], default=2, max_length=16, null=True, blank=True)),
                ('picture', stdimage.models.StdImageField(upload_to='media/images/profiles', null=True, blank=True)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('diets', models.ManyToManyField(related_name='diets', to='menus.Diet')),
                ('unlikes', models.ManyToManyField(to='menus.Ingredient')),
                ('unlikes_family', models.ManyToManyField(to='menus.IngredientFamily')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dom', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=128)),
                ('picture', stdimage.models.StdImageField(upload_to='media/images/recipe', null=True, blank=True)),
                ('origin_url', models.URLField()),
                ('prep_time', models.IntegerField()),
                ('cook_time', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('difficulty', models.IntegerField(choices=[(0, 'Très facile'), (1, 'Facile'), (2, 'Moyenne'), (3, 'Difficile')])),
                ('price', models.IntegerField(choices=[(0, 'Bon marché'), (1, 'Moyen'), (2, 'Assez cher')])),
                ('steps', models.TextField(null=True, blank=True)),
                ('detail', models.TextField(null=True, blank=True)),
                ('drink', models.TextField(null=True, blank=True)),
                ('category', models.CharField(default='Plat', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecipeToIngredient',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(default=None, null=True, blank=True)),
                ('unit', models.CharField(max_length=128, default=None, null=True, blank=True)),
                ('scraped_text', models.CharField(max_length=256, default=None, null=True, blank=True)),
                ('parsed_name', models.CharField(max_length=256, default=None, null=True, blank=True)),
                ('ingredient', models.ForeignKey(to='menus.Ingredient')),
                ('recipe', models.ForeignKey(to='menus.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='menus.RecipeToIngredient', to='menus.Ingredient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='unlikes_recipe',
            field=models.ManyToManyField(to='menus.Recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='profiles',
            field=models.ManyToManyField(to='menus.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='dessert',
            field=models.ForeignKey(related_name='dessert', to='menus.Recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='main_course',
            field=models.ForeignKey(related_name='main_course', to='menus.Recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='menu',
            field=models.ForeignKey(to='menus.Menu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='starter',
            field=models.ForeignKey(related_name='starter', to='menus.Recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingredientnutriment',
            name='nutriment',
            field=models.ForeignKey(to='menus.Nutriment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='family',
            field=models.ForeignKey(to='menus.IngredientFamily'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='nutriments',
            field=models.ManyToManyField(through='menus.IngredientNutriment', to='menus.Nutriment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diet',
            name='ingredients',
            field=models.ManyToManyField(to='menus.Ingredient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diet',
            name='ingredients_family',
            field=models.ManyToManyField(to='menus.IngredientFamily'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='guests',
            field=models.ManyToManyField(related_name='guests', to='menus.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='menus',
            field=models.ManyToManyField(to='menus.Menu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.OneToOneField(to='menus.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
