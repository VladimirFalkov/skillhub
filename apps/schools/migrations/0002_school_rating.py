# Generated by Django 3.2.6 on 2021-08-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='rating',
            field=models.IntegerField(choices=[(0, 'Нет рейтинга'), (1, 'Одна звезда'), (2, 'Две звезды'), (3, 'Три звезды'), (4, 'Четыре звезды'), (5, 'Пять звёзд')], default=3, verbose_name='Рейтинг'),
        ),
    ]
