from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from core.fields import AutoSlugField


class Course(models.Model):
    DRAFT = 1
    PUBLIC = 2
    STATUSES = (
        (DRAFT, _('Черновик')),
        (PUBLIC, _('Опубликован')),
    )

    ONLINE = 1
    OFFLINE = 2
    TYPE = [
        (ONLINE, _('Онлайн')),
        (OFFLINE, _('Оффлайн')),
    ]

    BEGINNER = 1
    ADVANCED = 2
    DIFFICULTY = [
        (BEGINNER, _('С нуля')),
        (ADVANCED, _('Продвинутый')),
    ]

    FREE = 1
    CHEAP = 2
    AVERAGE = 3
    EXPENSIVE = 4
    PRICE = [
        (FREE, _('Бесплатно')),
        (CHEAP, _('Низкая цена')),
        (AVERAGE, _('Средняя цена')),
        (EXPENSIVE, _('Высокая цена')),
    ]

    title = models.CharField(
        _('Название'),
        max_length=255,
    )
    url = models.URLField(
        _('Ссылка на страницу курса'),
    )
    affiliate_url = models.URLField(
        _('Партнёрская ссылка'),
        blank=True, null=True
    )
    category = models.ManyToManyField(
        'courses.Category',
        through='courses.CourseCategory',
        verbose_name=_('Категория'),
    )
    school = models.ForeignKey(
        'schools.School',
        models.CASCADE,
        verbose_name=_('Школа'),
    )
    type = models.PositiveIntegerField(
        _('Тип'),
        choices=TYPE,
        default=ONLINE,
    )
    difficulty = models.PositiveIntegerField(
        _('Уровень сложности'),
        choices=DIFFICULTY,
        default=BEGINNER,
    )
    price = models.PositiveIntegerField(
        _('Цена ₽'),
        choices=PRICE,
        default=AVERAGE,
    )
    price_details = models.TextField(
        _('Дополнительная информация о цене'),
        blank=True, null=True,
    )
    duration = models.PositiveIntegerField(
        _('Длительность, мес.'),
        blank=True, null=True,
    )
    status = models.PositiveSmallIntegerField(
        _('Статус'),
        choices=STATUSES,
        default=DRAFT,
    )
    author = models.ForeignKey(
        get_user_model(),
        models.CASCADE,
        verbose_name=_('Автор'),
        related_name='courses',
        blank=True, null=True,
    )
    start_anytime = models.BooleanField(
        _('Можно начать в любое время'),
        default=False,
    )
    installment = models.BooleanField(
        _('Возможна рассрочка'),
        default=False,
    )
    deferred_payment = models.BooleanField(
        _('Возможен отложенный платёж'),
        default=False,
    )
    created = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
    ),
    updated = models.DateTimeField(
        _('Дата обновлёния'),
        auto_now=True,
    )

    class Meta:
        db_table = 'course'
        verbose_name = _('Курс')
        verbose_name_plural = _('Курсы')

    def __str__(self):
        return self.title


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        models.CASCADE,
        related_name='children',
        verbose_name=_('Родительская категория'),
        blank=True, null=True,
    )
    title = models.CharField(
        _('Имя'),
        max_length=255,
    )
    slug = AutoSlugField(
        _('Слаг'),
        populate_from='name',
        unique=True,
    )
    description = models.TextField(
        _('Описание'),
        blank=True, null=True,
    )
    sort_order = models.IntegerField(
        _('Сортировка'),
        default=0,
    )

    class Meta:
        db_table = 'category'
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    course = models.ForeignKey(
        'courses.Course',
        models.CASCADE,
    )
    category = models.ForeignKey(
        'courses.Category',
        models.CASCADE,
    )

    class Meta:
        db_table = 'course_category'

    @property
    def course_count(self):
        categories = self.category.get_root().get_descendants(include_self=True)
        return Course.objects.filter(category__in=categories).count()
