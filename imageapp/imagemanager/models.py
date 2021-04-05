import os
import requests
from io import BytesIO
from PIL import Image as PilImage

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models


class Image(models.Model):
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
    url = models.URLField(verbose_name='Ссылка', max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.url and not self.image:
            image_name, image_extension = os.path.splitext(self.url)
            image_type = self.IMAGE_TYPES.get(image_extension.lower())

            response = requests.get(self.url)

            self.image = SimpleUploadedFile(
                name=f'{image_name}{image_extension}',
                content=response.content,
                content_type=image_type
            )

        super().save(*args, **kwargs)

    def resize(self, width: int, height: int) -> None:
        size = self._get_new_size(width, height)

        with BytesIO() as buffer:
            image_name, image_extension = os.path.splitext(self.image.name)
            image_type = self.IMAGE_TYPES.get(image_extension.lower())

            image = PilImage.open(self.image.path)
            image = image.resize(size, PilImage.ANTIALIAS)
            image.save(buffer, image_type)
            buffer.seek(0)

            self.resized_image = SimpleUploadedFile(
                name=f'{image_name}_resized{image_extension}',
                content=buffer.read(),
                content_type=image_type
            )

    def _get_new_size(self, width: int, height: int) -> tuple:
        if not width:
            width = height

        if not height:
            height = width

        width_ratio = width / self.image.width
        height_ratio = height / self.image.height

        if width_ratio < height_ratio:
            new_width = width
            new_height = round(width_ratio * self.image.height)
        else:
            new_width = round(height_ratio * self.image.width)
            new_height = height

        return (new_width, new_height)

    @property
    def filename(self) -> str:
        return os.path.basename(self.image.name)
