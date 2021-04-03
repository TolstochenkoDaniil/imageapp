from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from imagemanager.views import ImageUploadView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='/'),
    path('image_upload/', ImageUploadView.as_view(), name='image_upload')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
