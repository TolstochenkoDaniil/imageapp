from imagemanager.models import Image
from django import forms


class ImageUploadForm(forms.ModelForm):
    ''''''
    url = forms.URLField(required=False, label='Ссылка')

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if url and image:
            raise forms.ValidationError('Необходимо указать только один источник для изображения')

        return cleaned_data
    
    class Meta:
        model = Image
        fields = ('url', 'image')