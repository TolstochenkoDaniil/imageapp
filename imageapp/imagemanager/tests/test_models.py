import pytest
from io import BytesIO
from PIL import Image as img

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
    'size', [
        ((200,200)),
        ((200, 0)),
        ((0, 200))
    ]
)
def test_model_resize(fake_image, size, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    image = Image()
    image.image = fake_image
    image.save()

    image.resize(*size)

    assert image.resized_image.height == 200
    assert image.resized_image.width == 200
    
    assert image.resized_image.url is not None


def test_upload_image_with_url(tmp_path):
    settings.MEDIA_ROOT = tmp_path
    image = Image()
    image.url = 'https://cdn.vox-cdn.com/thumbor/FOIV1c1Eq9Y1HQq-Sn1RgReLp0E=/0x0:735x500/920x613/filters:focal(310x192:426x308):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/66727168/image.0.png'

    image.save()

    assert image.image.name is not None