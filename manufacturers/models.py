from django.db import models
from products.models import categories
from astra.functions import get_file_path, image_help_text, resize_img
from django.utils.functional import cached_property
from django.utils.html import format_html


class manufacturer_page(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    menu_name = models.CharField('Название в меню', max_length=1000)
    section_title = models.CharField('Название раздела', max_length=1000)

    def __str__(self):
        return 'Общая страница'

    class Meta:
        verbose_name = 'Общая страница'
        verbose_name_plural = 'Общая страница'


class country(models.Model):

    title = models.CharField('Страна', max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class man_categories(models.Model):

    title = models.CharField('Категория', max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория производителей'
        verbose_name_plural = 'Категории производителей'


class manufacturers(models.Model):

    order = models.IntegerField('Порядок')

    show_about = models.BooleanField('Отображать на странице "О нас"', default=False)

    man_categories = models.ForeignKey(man_categories, null=True, verbose_name='Выбрать категорию на главной странице', blank=True, on_delete=models.CASCADE, related_name='main_page_categories')

    categories = models.ManyToManyField(categories, verbose_name='Выбрать категорию', related_name='manufacturer_categories')
    country = models.ForeignKey(country, verbose_name='Выбрать страну', on_delete=models.CASCADE, related_name='manufacturer_country')
    name = models.CharField('Наименование производителя', max_length=1000, blank=True)
    link = models.CharField('Ссылка', max_length=1000, blank=True)

    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text, blank=True)
    image_png2x = models.ImageField(upload_to=get_file_path, blank=True)
    image_png = models.ImageField(upload_to=get_file_path, blank=True)
    image_about = models.ImageField(upload_to=get_file_path, blank=True)

    __original_image = None

    def __init__(self, *args, **kwargs):
        super(manufacturers, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and self.image != self.__original_image:
            self.image_about = resize_img(self.image_about, self.image, 800, 'png', 'transparent')
            self.image_png2x = resize_img(self.image_png2x, self.image, 300, 'png', 'transparent')
            self.image_png = resize_img(self.image_png, self.image, 150, 'png', 'transparent')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'

    def image_tag(self):
        from django.utils.html import mark_safe
        if self.image:
            return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.image.url))
    image_tag.short_description = 'Изображение'





