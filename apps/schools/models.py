from ckeditor.fields import RichTextField

from django.db import models
from django.utils.translation import gettext_lazy as _


class School(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=255,
    )
    description = RichTextField(
        _('Описание'),
        blank=True, null=True,
    )
    accredited = models.BooleanField(
        _('Аккредитованное учебное заведение'),
        default=False,
    )
    rating = models.FloatField(
        _('Рейтинг'),
        default=0,
    )
    epc = models.FloatField(
        _('Средний заработок с перехода'),
        default=0
    )
    is_active = models.BooleanField(
        _('Активный'),
        default=False,
    )

    class Meta:
        db_table = 'school'
        verbose_name = _('Школа')
        verbose_name_plural = _('Школы')

    def __str__(self):
        return self.name


class SchoolAlias(models.Model):
    name = models.CharField(
        _('Имя'),
        max_length=255,
    )
    school = models.ForeignKey(
        'schools.School',
        models.CASCADE,
        related_name='aliases',
        verbose_name=_('Школа'),
    )
    source = models.ForeignKey(
        'sources.DataSource',
        models.CASCADE,
        verbose_name=_('Источник данных'),
    )
    disabled = models.BooleanField(
        _('Отключен'),
        default=False,
    )
    
    class Meta:
        verbose_name = _('Псевдоним школы')
        verbose_name_plural = _('Псевдонимы школ')
        unique_together = (
            ('school', 'source'),
        )

    def __str__(self):
        return self.name


class Advantages(models.Model):
    title = models.CharField(
        _('Заголовок'),
        max_length=255,
    )
    description = models.TextField(
        _('Описание'),
    )
    school = models.ForeignKey(
        'schools.School',
        models.CASCADE,
        related_name='advantages',
        verbose_name=_('Школа'),
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
    )

    class Meta:
        verbose_name = _('Преимущество школы')
        verbose_name_plural = _('Преимущества школ')

    def __str__(self):
        return self.title


class Disadvantages(models.Model):
    title = models.CharField(
        _('Заголовок'),
        max_length=255,
    )
    description = models.TextField(
        _('Описание'),
    )
    school = models.ForeignKey(
        'schools.School',
        models.CASCADE,
        related_name='disadvantages',
        verbose_name=_('Школа'),
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
    )

    class Meta:
        verbose_name = _('Недостаток школы')
        verbose_name_plural = _('Недостатки школ')
    
    def __str__(self):
        return self.title