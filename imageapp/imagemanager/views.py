import types
from typing import Type
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from imagemanager.models import Image
from imagemanager.forms import ImageUploadForm, ImageEditForm


class ImageUploadView(CreateView):
    ''''''
    template_name = 'imagemanager/upload.html'
    form_class = ImageUploadForm
    model = Image

    def get_success_url(self) -> str:
        return reverse('edit_image', kwargs={'pk': self.object.pk})


class ImageEditView(UpdateView):
    ''''''
    template_name = 'imagemanager/edit.html'
    form_class = ImageEditForm
    model = Image

    def __init__(self, *args, **kwargs) -> None:
        self.resized_image = None
        super().__init__(*args, **kwargs)

    def get_success_url(self) -> str:
        return self.request.path

    def form_valid(self, form: Type[ImageEditForm]) -> HttpResponse:
        height = form.cleaned_data.get('height', 0)
        width = form.cleaned_data.get('width', 0)

        image = self.get_object()
        image.resize(height, width)

        return super().form_valid(form)


class ImageListView(ListView):
    ''''''
    model = Image