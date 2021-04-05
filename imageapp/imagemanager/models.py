import os
import requests
from io import BytesIO
from PIL import Image as img

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.db import models


class Image(models.Model):
    ''''''
    IMAGE_TYPES = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.gif': 'GIF',
        '.png': 'PNG'
    }

    image = models.ImageField(
        upload_to='images',
        verbose_name='Файл',
        null=True,
        blank=True
    )
    resized_image = models.ImageField(
        upload_to='images',
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

        with BytesIO() as buffer:
            image_name, image_extension = os.path.splitext(self.image.name)

            image_type = self.IMAGE_TYPES.get(image_extension.lower())

            image = img.open(self.image.path)
            image.thumbnail(size, img.ANTIALIAS)
            image.save(buffer, image_type)
            buffer.seek(0)
            
            self.resized_image = SimpleUploadedFile(
                name=f'{image_name}_resized{image_extension}',
                content=buffer.read(),
                content_type=image_type
            )

    @property
    def filename(self):
        return os.path.basename(self.image.name)
