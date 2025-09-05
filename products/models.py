from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from astra.functions import get_file_path, image_help_text, svg_help_text, resize_img, make_slug, pdf_help_text
from django.utils.html import format_html
from django.utils.functional import cached_property
from django.core.validators import FileExtensionValidator


class filters(models.Model):

    filter_title = models.CharField('Наименование бренда', max_length=1000)

    def __str__(self):
        return self.filter_title

    class Meta:
        ordering = ['filter_title']
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'


class filters_parameters(models.Model):

    filters = models.ForeignKey(filters, on_delete=models.CASCADE, related_name='filters_parameters')

    parameter_title = models.CharField('Значение', max_length=1000)

    def __str__(self):
        return self.filters.filter_title + ': ' + self.parameter_title

    class Meta:
        ordering = ['parameter_title']
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'


class catalog_page(models.Model):

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    menu_name = models.CharField('Название в меню', max_length=1000)
    section_title = models.CharField('Название раздела', max_length=1000)

    main_subtitle = models.TextField('Подзаголовок', blank=True)

    seo = RichTextField('Текст для SEO', blank=True)

    dostavka = RichTextField('Оплата и доставка', blank=True)

    def __str__(self):
        return 'Общая страница каталога'

    class Meta:
        verbose_name = 'Общая страница каталога'
        verbose_name_plural = 'Общая страница каталога'


class brands(models.Model):

    brand_title = models.CharField('Наименование бренда', max_length=1000)

    def __str__(self):
        return self.brand_title

    class Meta:
        ordering = ['-brand_title']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class countries(models.Model):

    country_title = models.CharField('Наименование бренда', max_length=1000)

    def __str__(self):
        return self.country_title

    class Meta:
        ordering = ['-country_title']
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class categories(models.Model):

    order = models.IntegerField('Порядок')

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    cat_title = models.CharField('Наименование категории', max_length=1000)
    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text)
    image_2x_webp = models.ImageField(upload_to=get_file_path, blank=True)
    image_2x_jpg = models.ImageField(upload_to=get_file_path, blank=True)
    image_webp = models.ImageField(upload_to=get_file_path, blank=True)
    image_jpg = models.ImageField(upload_to=get_file_path, blank=True)
    slug = models.SlugField('URL', max_length=50, allow_unicode=True, unique=True, blank=True)


    __original_image = None

    seo = RichTextField('Текст для SEO', blank=True)

    def __init__(self, *args, **kwargs):
        super(categories, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = make_slug(self.slug, self.cat_title, categories, self.id)
        if self.image and self.image != self.__original_image:
            self.image_2x_webp = resize_img(self.image_2x_webp, self.image, [832, 420], 'webp')
            self.image_2x_jpg = resize_img(self.image_2x_jpg, self.image, [832, 420], 'jpeg')
            self.image_webp = resize_img(self.image_webp, self.image, [416, 210], 'webp')
            self.image_jpg = resize_img(self.image_jpg, self.image, [416, 210], 'jpeg')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cat_title

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'


class subcategories(models.Model):

    order = models.IntegerField('Порядок')

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    categories = models.ForeignKey(categories, verbose_name='Выбрать категорию', on_delete=models.CASCADE, related_name='categories')

    subcategory_title = models.CharField('Наименование подкатегории', max_length=1000)

    subcategory_description = RichTextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text, blank=True)
    image_2x_webp = models.ImageField(upload_to=get_file_path, blank=True)
    image_2x_jpg = models.ImageField(upload_to=get_file_path, blank=True)
    image_webp = models.ImageField(upload_to=get_file_path, blank=True)
    image_jpg = models.ImageField(upload_to=get_file_path, blank=True)
    icon = models.FileField('Иконка', upload_to=get_file_path, help_text=svg_help_text)
    manufacturers = models.ManyToManyField('manufacturers.manufacturers', verbose_name='Выбрать производителей', related_name='subcategories_manufacturers')
    slug = models.SlugField('URL', max_length=50, allow_unicode=True, unique=True, blank=True)

    __original_image = None

    seo = RichTextField('Текст для SEO', blank=True)

    def __init__(self, *args, **kwargs):
        super(subcategories, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = make_slug(self.slug, self.subcategory_title, subcategories, self.id)
        if self.image and self.image != self.__original_image:
            self.image_2x_webp = resize_img(self.image_2x_webp, self.image, [1056, 760], 'webp')
            self.image_2x_jpg = resize_img(self.image_2x_jpg, self.image, [1056, 760], 'jpeg')
            self.image_webp = resize_img(self.image_webp, self.image, [528, 380], 'webp')
            self.image_jpg = resize_img(self.image_jpg, self.image, [528, 380], 'jpeg')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subcategory_title

    class Meta:
        ordering = ['order']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'

    @cached_property
    def display_icon(self):
        return format_html('<img src="{img}" width="300">', img=self.icon.url)
    display_icon.short_description = 'Предпросмотр иконки'


class product(models.Model):

    order = models.IntegerField('Порядок')

    title = models.CharField('Заголовок', max_length=1000)
    description = models.CharField('Описание', max_length=1000, blank=True)
    keywords = models.CharField('Ключевые слова', max_length=1000, blank=True)

    subcategories = models.ForeignKey(subcategories, verbose_name='Выбрать подкатегорию', on_delete=models.SET_NULL,
                                      null=True, related_name='products_subcategory', blank=True)

    leftovers = models.BooleanField('Складские остатки', default=True, blank=True)
    pop_models = models.BooleanField('Популярные модели', default=True, blank=True)

    product_title = models.CharField('Наименование продукта', max_length=1000)
    product_description = RichTextField('Описание', blank=True)
    product_price = models.FloatField('Стоимость продукта за 1 шт', default=1, blank=True, null=True)

    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text, blank=True)
    image_detail_png2x = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    image_detail_png = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    image_detail_webp = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    image_other_png2x = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    image_other_png = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    image_other_webp = models.ImageField('Изображение', upload_to=get_file_path, blank=True)
    slug = models.SlugField('URL', max_length=50, allow_unicode=True, unique=True, blank=True)

    __original_image = None

    instock = models.BooleanField('В наличии', default=True, blank=True)
    article = models.CharField('Артикул', max_length=1000)
    brands = models.ForeignKey(brands, verbose_name='Бренд', on_delete=models.CASCADE, related_name='product_brands')
    countries = models.ForeignKey(countries, verbose_name='Страна', on_delete=models.CASCADE, related_name='product_country')

    filters = models.ManyToManyField(filters_parameters, verbose_name='Значения фильтров', blank=True, related_name='products_filters')

    seo = RichTextField('Текст для SEO', blank=True)

    def __init__(self, *args, **kwargs):
        super(product, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = make_slug(self.slug, self.product_title, product, self.id)
        if self.image and self.image != self.__original_image:
            self.image_detail_png2x = resize_img(self.image_detail_png2x, self.image, [832, 614], 'jpeg')
            self.image_detail_png = resize_img(self.image_detail_png, self.image, [416, 307], 'jpeg')
            self.image_detail_webp = resize_img(self.image_detail_webp, self.image, [832, 614], 'webp')
            self.image_other_png2x = resize_img(self.image_other_png2x, self.image, [608, 450], 'jpeg')
            self.image_other_png = resize_img(self.image_other_png, self.image, [304, 225], 'jpeg')
            self.image_other_webp = resize_img(self.image_other_webp, self.image, [608, 450], 'webp')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_title

    class Meta:
        ordering = ['order']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'



class product_parameters(models.Model):

    order = models.IntegerField('Порядок')

    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_parameters')

    title = models.CharField('Параметр', max_length=1000)
    subtitle = models.CharField('Значение', max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


class product_chars(models.Model):

    order = models.IntegerField('Порядок')

    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_chars')

    title = models.TextField('Характеристика')
    subtitle = RichTextField('Значение')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class faq_catalogue_page(models.Model):

    order = models.IntegerField('Порядок')

    catalog_page = models.ForeignKey(catalog_page, on_delete=models.CASCADE, related_name='faq_catalog_page')

    question = models.CharField('Вопрос', max_length=1000)
    answer = RichTextField('Ответ')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class faq_categories(models.Model):

    order = models.IntegerField('Порядок')

    categories = models.ForeignKey(categories, on_delete=models.CASCADE, related_name='faq_categories')

    question = models.CharField('Вопрос', max_length=1000)
    answer = RichTextField('Ответ')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class faq_subcategories(models.Model):

    order = models.IntegerField('Порядок')

    subcategories = models.ForeignKey(subcategories, on_delete=models.CASCADE, related_name='faq_subcategories')

    question = models.CharField('Вопрос', max_length=1000)
    answer = RichTextField('Ответ')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class product_slider(models.Model):

    order = models.IntegerField('Порядок')

    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_slider')

    image = models.ImageField('Изображение', upload_to=get_file_path, help_text=image_help_text)
    __original_image = None

    alt = models.CharField('alt-тег', max_length=500)

    def __init__(self, *args, **kwargs):
        super(product_slider, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and self.image != self.__original_image:
            self.image = resize_img(self.image, self.image, 1024, 'jpeg')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    @cached_property
    def display_image(self):
        return format_html('<img src="{img}" width="300">', img=self.image.url)
    display_image.short_description = 'Предпросмотр изображения'


class product_file(models.Model):

    order = models.IntegerField('Порядок')

    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_file')

    file = models.FileField('Документ', upload_to=get_file_path, help_text=pdf_help_text,
                                 validators=[FileExtensionValidator(['pdf'])])

    name = models.CharField('Название', max_length=500)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['order']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'










