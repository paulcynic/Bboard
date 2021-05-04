from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное', code='odd', params={'value': val})


# class MinMaxValueValidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = min_value
#         self.max_value = max_value
#
#     def __call__(self, val):
#         if val < self.min_value or val > self.max_value:
#             raise ValidationError('Введенное число должно находиться в диапазоне от %(min)s до %(max)s',
#                                   code='out_of_range', params={'min': self.min_value, 'max': self.max_value})


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Деталь')


class Machine(models.Model):
    name = models.CharField(max_length=30, null=True, verbose_name='Автомобиль')
    spares = models.ManyToManyField(Spare, null=True, blank=True)


class Measure(models.Model):
    class Measurements(float, models.Choices):
        METERS = (1.0, 'Метры')
        FEET = (0.3048, 'Футы')
        YARDS = (0.9144, 'Ярды')
    measurement = models.FloatField(choices=Measurements.choices)


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['order', 'name']


class Bb(models.Model):
    KINDS = (
        ('Купля-продажа', (
            ('b', 'куплю'),
            ('s', 'продам'),
        )),
        ('Обмен', (
            ('c', 'обменяю'),
        )),
        (None, 'Выберите пункт публикуемого объявления'),
    )
    kind = models.CharField(max_length=1, choices=KINDS, default='s', blank=True, verbose_name='Раздел')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, related_name='entries', verbose_name='Рубрика')
    title = models.CharField(max_length=50, validators=[validators.RegexValidator(regex='^.{3,}$')],
                             error_messages={'invalid': 'Название содержит менее трёх букв!'}, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True,
                                validators=[validate_even], verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def title_and_price(self):
        if self.price:
            return '%s (%s)' % (self.title, self.price)
        else:
            return self.title

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        # order_with_respect_to = 'rubric'
        # get_latest_by = ['published']
        ordering = ['-published']
        unique_together = (
            ('title', 'published'),
            ('title', 'price', 'rubric'),
        )
        # index_together = [
        #     ['title', 'published'],
        #     ['title', 'price', 'rubric'],
        # ]
        # indexes = [
        #     models.Index(fields=['title', '-published'], name='bb_name'),
        #     models.Index(fields=['title', 'price', 'rubric']),
        # ]


def clean(self):
    errors = {}
    if not self.content:
        errors['content'] = ValidationError('Укажите описание продаваемого товара')
    if self.price and self.price < 0:
        errors['price'] = ValidationError('Укажите неотрицательное значение цены')
    if errors:
        raise ValidationError(errors)
