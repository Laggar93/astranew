from django.core.validators import FileExtensionValidator
from django.db import models
from astra.functions import get_file_path, pdf_help_text


class contacts(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    menu_name = models.CharField('Название в меню', max_length=1000)
    section_title = models.CharField('Название раздела', max_length=1000)

    address = models.TextField('Адрес')

    first_phone = models.CharField('Телефон #1', max_length=1000, blank=True)
    second_phone = models.CharField('Телефон #2', max_length=1000, blank=True)
    header_phone = models.CharField('Телефон в шапке сайта', max_length=1000, blank=True)

    email = models.CharField('Email', max_length=1000, blank=True)

    telegram = models.CharField('Telegram', max_length=1000, blank=True)
    whatsapp = models.CharField('Whatsapp', max_length=1000, blank=True)

    first_file = models.FileField('Согласие на обработку персональных данных', help_text=pdf_help_text,
                                 validators=[FileExtensionValidator(['pdf'])])

    second_file = models.FileField('Положение по работе с персональными данными', help_text=pdf_help_text,
                                  validators=[FileExtensionValidator(['pdf'])])

    third_file = models.FileField('Политика использования файлов cookies', help_text=pdf_help_text,
                                   validators=[FileExtensionValidator(['pdf'])])

    fourth_file = models.FileField('Согласие на обработку персональных данных, собираемых метрическими системами', help_text=pdf_help_text,
                                  validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return 'Общая страница'

    class Meta:
        verbose_name = 'Общая страница'
        verbose_name_plural = 'Общая страница'


class requisites(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    subtitle = models.TextField('Подзаголовок')

    def __str__(self):
        return 'Реквизиты'

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'


class requisites_items(models.Model):

    order = models.IntegerField('Порядок')

    requisites = models.ForeignKey(requisites, on_delete=models.CASCADE, related_name='requisites_items')

    title = models.CharField('Заголовок', max_length=1000, blank=True)
    subtitle = models.TextField('Подзаголовок', blank=True)

    def __str__(self):
        return 'Реквизиты'

    class Meta:
        ordering = ['order']
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'
