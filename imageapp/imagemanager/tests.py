import pytest
from io import BytesIO
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from imagemanager.forms import ImageUploadForm


@pytest.fixture
def files(request):
    if request.param:
        image_file = BytesIO()
        image = Image.new('RGBA', size=(50,50), color=(256,0,0))
        image.save(image_file, 'png')
        image_file.seek(0)

        return {'image': SimpleUploadedFile(name='test.png', content=image_file.read())}

    return {}


@pytest.mark.parametrize(
    'data, files',
    [
        ({'url': 'http://example.com'}, None),
        ({'url': None}, 'png'),
    ],
    indirect=['files'],
)
def test_imageform_is_valid(data, files):
    form = ImageUploadForm(data, files)

    assert form.is_valid() == True


@pytest.mark.parametrize(
    'data, files',
    [
        ({'url': 'http://example.com'}, 'png')
    ],
    indirect=['files'],
)
def test_imageform_raises_error(data, files):
    form = ImageUploadForm(data, files)

    with pytest.raises(forms.ValidationError):
        form.is_valid()
        form.clean()