import os
from io import BytesIO
from PIL import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.db import models
import requests


class Image(models.Model):
    ''''''
    image = models.ImageField(
        upload_to='images',
        verbose_name='Файл',
        null=True,
        blank=True
    )
    resized_image = models.ImageField(
        upload_to='resized_images',
        verbose_name='Отформатированное изображение',
        null=True,
        blank=True
    )
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.url:
            response = requests.get(self.url)
            self.image = SimpleUploadedFile(name='', content=response.content)

        super().save(*args, **kwargs)

    def resize(self, height, width):
        ''''''
        if not height:
            height = width

        if not width:
            width = height

        size = (height, width)
        buffer = BytesIO()
        extention = os.path.splitext(self.image.name)[1].replace(".", "")

        if extention.upper() == 'JPG':
            extention = 'JPEG'

        image = img.open(self.image.path)
        image.thumbnail(size, img.ANTIALIAS)
        image.save(buffer, extention)

        self.resized_image.save(os.path.basename(self.image.name), File(buffer), save=False)
        buffer.close()

    @property
    def filename(self):
        return os.path.basename(self.image.name)
