import os
import sys
import uuid
from io import BytesIO
from pytils.translit import slugify
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import random, string
from django.conf import settings
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from .config import send_email


quality = 70
reduce = None


def get_file_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)


def make_slug(slug, field, model, elem, add=None):

    if not slug:
        slug = slugify(field)[:50]

    if model.objects.filter(slug=slug).count() >= 1 and not model.objects.filter(slug=slug, id=elem):
        if add:
            slug = slug + slugify(add)
            if model.objects.filter(slug=slug).count() >= 1 and not model.objects.filter(slug=slug, id=elem):
                slug = slug + slugify(''.join(random.choice(string.ascii_letters) for x in range(3)))
        else:
            slug = slug + slugify(''.join(random.choice(string.ascii_letters) for x in range(3)))
    
    return slug


def resize_img(f1, f2, fs, format=None, color=None):

    ext = str(f1).split('.')[-1]

    is_array = True
    f1 = f2
    image1 = f1
    img1 = Image.open(image1)
    if color == 'transparent' and format == 'png' or color == 'transparent' and format == 'webp':
        new_img1 = img1.convert('RGBA')
    else:
        img1 = img1.convert('RGBA')
        if color:
            background = Image.new(img1.mode[:-1], img1.size, color)
        else:
            background = Image.new(img1.mode[:-1], img1.size, (255, 255, 255))
        background.paste(img1, img1.split()[-1])
        img1 = background
        new_img1 = img1.convert('RGB')

    try:
        fs[0]
    except:
        is_array = False
    
    if reduce:
        if is_array:
            fs[0] = int(fs[0] * reduce)
            fs[1] = int(fs[1] * reduce)
        else:
            fs = int(fs * reduce)

    if is_array:
        ratio_current = new_img1.size[1] / new_img1.size[0]
        ratio_new = fs[1] / fs[0]
        if ratio_current <= ratio_new:
            new_width = (fs[1] * new_img1.size[0]) / new_img1.size[1]
            new_height = fs[1]
            resized_new_img1 = new_img1.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            box = ((resized_new_img1.size[0] - fs[0]) / 2, 0, resized_new_img1.size[0] - (resized_new_img1.size[0] - fs[0]) / 2, resized_new_img1.size[1])
            resized_new_img1 = resized_new_img1.crop(box)
        else:
            new_width = fs[0]
            new_height = (new_img1.size[1] * fs[0]) / new_img1.size[0]
            resized_new_img1 = new_img1.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            box = (0, (resized_new_img1.size[1] - fs[1]) / 2, resized_new_img1.size[0], resized_new_img1.size[1] - (resized_new_img1.size[1] - fs[1]) / 2)
            resized_new_img1 = resized_new_img1.crop(box)

    else:

        img_w = new_img1.size[0]
        img_h = new_img1.size[1]

        if img_w >= img_h:
            height = int(fs / (img_w / img_h))
            resize_size = [fs, height]
        else:
            width = int(fs / (img_h / img_w))
            resize_size = [width, fs]
        
        resized_new_img1 = new_img1.resize(resize_size, Image.ANTIALIAS)

    filestream1 = BytesIO()

    if ext != 'webp':
        if ext == 'jpg' or ext == 'jpeg':
            ext = 'JPEG'
        if ext == 'png':
            ext = 'PNG'
        else:
            ext = 'JPEG'
    else:
        ext = 'WEBP'
    
    if format:
        ext = format.upper()

    if color == 'transparent':
        resized_new_img1.save(filestream1, ext)
    else:
        resized_new_img1.save(filestream1, ext, optimize=True, quality=quality)

    filestream1.seek(0)
    name1 = f"{f1.name}"
    if format:
        name1 = name1.replace(name1.split('.')[1], format)
        filestream_format = format + '/image'
    else:
        filestream_format = 'jpeg' + '/image'

    return InMemoryUploadedFile(
        filestream1, 'ImageField', name1, filestream_format,
        sys.getsizeof(filestream1), None
    )


slug_help_text = 'URL генерируется автоматически из названия раздела, но может быть задан вручную'
image_help_text = 'Формат файла: JPG, JPEG, PNG или WEBP. Ограничение размера: 3 Мбайт.'
video_help_text = 'Формат файла: MP4. Ограничение размера: 20 Мбайт.'
pdf_help_text = 'Формат файла: PDF. Ограничение размера: 20 Мбайт.'
svg_help_text = 'Формат файла: SVG. Ограничени размера: 500 Кбайт.'


def send_order(name, phone, email, message):

    topic = 'Заявка с сайта'
    body = '<p>Имя: ' + name + '</p><p>Телефон: ' + phone + '</p><p>E-mail: ' + email + '</p><p>Сообщение:</p><p>' + message + '</p>'
    
    send_msg = EmailMessage(topic, body, settings.EMAIL_HOST_USER, send_email)
    send_msg.content_subtype = "html"
    send_msg.send()

    return HttpResponse('success')