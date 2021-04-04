from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from imagemanager.views import ImageUploadView, ImageEditView, ImageListView


urlpatterns = [
    path('', ImageListView.as_view(template_name='home.html'), name='/'),
    path('image/upload', ImageUploadView.as_view(), name='upload_image'),
    path('image/<int:pk>/edit', ImageEditView.as_view(), name='edit_image')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
