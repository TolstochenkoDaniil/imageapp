import pytest
from io import BytesIO
from PIL import Image as img
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from imagemanager.models import Image


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def fake_image():
    image_file = BytesIO()
    image = img.new('RGBA', size=(500,500), color=(256,0,0))
    image.save(image_file, 'png')
    image_file.seek(0)

    return SimpleUploadedFile(name='test.png', content=image_file.read())


@pytest.mark.parametrize(
    'size', [((200,200))]
)
def test_model_resize(fake_image, size, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    image = Image()
    image.image = fake_image
    image.save()

    resized_image = image.resize(*size)

    assert resized_image.size == size


@pytest.mark.parametrize(
    'size', [((200,200))]
)
def test_model_get_resized_image(fake_image, size, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    image = Image()
    image.image = fake_image
    image.save()

    image_uri = image.get_resized_image(*size)

    assert isinstance(image_uri, str) == True