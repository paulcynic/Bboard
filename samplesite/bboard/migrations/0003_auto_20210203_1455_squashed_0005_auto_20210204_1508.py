# Generated by Django 3.1.5 on 2021-02-07 04:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('bboard', '0003_auto_20210203_1455'), ('bboard', '0004_auto_20210203_1714'), ('bboard', '0005_auto_20210204_1508')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0002_auto_20210121_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bb',
            options={'get_latest_by': ['published'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AddField(
            model_name='bb',
            name='kind',
            field=models.CharField(blank=True, choices=[('Купля-продажа', (('b', 'куплю'), ('s', 'продам'))), ('Обмен', (('c', 'обменяю'),)), (None, 'Выберите пункт публикуемого объявления')], default='s', max_length=1),
        ),
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='Цена'),
        ),
        migrations.AlterUniqueTogether(
            name='bb',
            unique_together={('title', 'price', 'rubric'), ('title', 'published')},
        ),
        migrations.AlterModelOptions(
            name='bb',
            options={},
        ),
        migrations.AlterField(
            model_name='bb',
            name='kind',
            field=models.CharField(blank=True, choices=[('Купля-продажа', (('b', 'куплю'), ('s', 'продам'))), ('Обмен', (('c', 'обменяю'),)), (None, 'Выберите пункт публикуемого объявления')], default='s', max_length=1, verbose_name='Раздел'),
        ),
        migrations.AlterUniqueTogether(
            name='bb',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'invalid': 'Неправильное название товара'}, max_length=50, validators=[django.core.validators.RegexValidator(regex='^.{4,}$')], verbose_name='Товар'),
        ),
    ]
