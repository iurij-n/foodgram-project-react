# Generated by Django 3.2.13 on 2022-06-26 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='media/recipes/images/', verbose_name='Картинка для рецепта'),
        ),
    ]
