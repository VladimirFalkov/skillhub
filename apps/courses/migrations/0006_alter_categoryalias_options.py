# Generated by Django 3.2.9 on 2021-11-29 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20211113_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryalias',
            options={'verbose_name': 'Псевдоним категории', 'verbose_name_plural': 'Псевдонимы категорий'},
        ),
    ]
