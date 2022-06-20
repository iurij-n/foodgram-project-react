# Generated by Django 2.2 on 2022-06-15 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(default=1, help_text='Избранный рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipe.Recipe', verbose_name='Избранный рецепт'),
            preserve_default=False,
        ),
    ]