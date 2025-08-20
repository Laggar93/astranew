from django.db import models
from astra.functions import get_file_path, image_help_text, resize_img
from django.utils.html import format_html
from django.utils.functional import cached_property


class about_page(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    menu_name = models.CharField('Название в меню', max_length=1000)
    section_title = models.CharField('Название раздела', max_length=1000)

    first_subtitle = models.TextField('Верхний подзаголовок', blank=True)
    second_subtitle = models.TextField('Нижний подзаголовок', blank=True)

    def __str__(self):
        return 'Общая страница'

    class Meta:
        verbose_name = 'Общая страница'
        verbose_name_plural = 'Общая страница'


class about_rules(models.Model):

    title = models.CharField('Заголовок', max_length=1000)

    def __str__(self):
        return 'Принципы компании'

    class Meta:
        verbose_name = 'Принципы компании'
        verbose_name_plural = 'Принципы компании'


class about_rules_items(models.Model):

    order = models.IntegerField('Порядок')

    about_rules = models.ForeignKey(about_rules, on_delete=models.CASCADE, related_name='about_rules_items')

    title = models.CharField('Заголовок', max_length=1000)
    subtitle = models.TextField('Подзаголовок')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Принцип компании'
        verbose_name_plural = 'Принципы компании'


class about_manufacturers(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    subtitle = models.TextField('Подзаголовок', blank=True)

    def __str__(self):
        return 'Партнеры компании'

    class Meta:
        verbose_name = 'Партнер компании'
        verbose_name_plural = 'Партнеры компании'


class about_team(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    subtitle = models.TextField('Подзаголовок', blank=True)

    def __str__(self):
        return 'Команда'

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команда'


class about_team_items(models.Model):

    order = models.IntegerField('Порядок')

    about_team = models.ForeignKey(about_team, on_delete=models.CASCADE, related_name='about_team_items')

    name = models.CharField('ФИО', max_length=1000)
    position = models.CharField('Должность', max_length=1000)
    email = models.EmailField('Email', blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text, blank=True)
    image_png2x = models.ImageField(upload_to=get_file_path, blank=True)
    image_png = models.ImageField(upload_to=get_file_path, blank=True)

    __original_image = None

    def __init__(self, *args, **kwargs):
        super(about_team_items, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and self.image != self.__original_image:
            self.image_png2x = resize_img(self.image_png2x, self.image, [608, 652], 'jpeg')
            self.image_png = resize_img(self.image_png, self.image, [304, 326], 'jpeg')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команды'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'


class about_supplies(models.Model):

    title = models.CharField('Заголовок', max_length=1000)

    def __str__(self):
        return 'География поставок'

    class Meta:
        verbose_name = 'География поставок'
        verbose_name_plural = 'География поставок'


class about_supplies_items(models.Model):

    order = models.IntegerField('Порядок')

    about_supplies = models.ForeignKey(about_supplies, on_delete=models.CASCADE, related_name='about_supplies_items')

    count = models.CharField('Количество', max_length=1000)
    title = models.CharField('Описание', max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'География поставок'
        verbose_name_plural = 'География поставок'












