from ckeditor.fields import RichTextField
from django.db import models


class main_page(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    main_title = RichTextField('Заголовок на видео')

    def __str__(self):
        return 'Общая страница'

    class Meta:
        verbose_name = 'Общая страница'
        verbose_name_plural = 'Общая страница'


class main_page_items(models.Model):

    order = models.IntegerField('Порядок')

    main_page = models.ForeignKey(main_page, on_delete=models.CASCADE, related_name='main_page_items')

    title = models.TextField('Заголовок')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
