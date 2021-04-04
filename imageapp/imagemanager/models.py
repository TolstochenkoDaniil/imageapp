import os
import base64
from io import BytesIO
from PIL import Image as img
from django.db import models


class Image(models.Model):
    ''''''
    image = models.ImageField(upload_to='images', verbose_name='Файл', null=True, blank=True)

    def get_resized_image(self, heigth, width):
        data = BytesIO()
        extension = os.path.splitext(self.image.name)[1].replace(".", "")

        image = self.resize(heigth, width)
        image.save(data, extension)

        encoded_image = base64.b64encode(data.getvalue())
        decoded_image = encoded_image.decode('utf-8')

        return f"data:image/{extension};base64,{decoded_image}"

    def resize(self, heigth, width):
        ''''''
        size = (heigth, width)

        image = img.open(self.image.path)
        image.thumbnail(size, img.ANTIALIAS)

        return image

    @property
    def filename(self):
        return os.path.basename(self.image.name)
