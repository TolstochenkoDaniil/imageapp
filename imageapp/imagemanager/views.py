from django.views.generic.edit import CreateView

from imagemanager.models import Image
from imagemanager.forms import ImageUploadForm


class ImageUploadView(CreateView):
    ''''''
    template_name = 'imagemanager/path_form.html'
    form_class = ImageUploadForm
    model = Image
    
    def get_success_url(self) -> str:
        return self.request.path