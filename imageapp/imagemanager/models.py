from django.db import models


class Image(models.Model):
    ''''''
    image = models.ImageField(upload_to='images', verbose_name='Файл', blank=True)
