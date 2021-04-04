from django import forms

from imagemanager.models import Image


class ImageUploadForm(forms.ModelForm):
    ''''''
    url = forms.URLField(required=False, label='Ссылка')

    class Meta:
        model = Image
        fields = ('url', 'image')

    def clean(self):
        self.cleaned_data = super().clean()

        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')

        if url and image:
            raise forms.ValidationError('Необходимо указать только один источник для изображения')

        if not url and not image:
            raise forms.ValidationError('Необходимо указать хотя бы один источник для изображения')

        return self.cleaned_data


class ImageEditForm(forms.ModelForm):
    ''''''
    width = forms.IntegerField(label='Ширина', required=False)
    heigth = forms.IntegerField(label='Высота', required=False)

    class Meta:
        model = Image
        fields = ('width', 'heigth')
        exclude = ('image',)
        
    def clean(self):
        self.cleaned_data = super().clean()

        width = self.cleaned_data.get('width')
        heigth = self.cleaned_data.get('heigth')

        if not (width and heigth):
            raise forms.ValidationError('Необходимо указать хотя бы один параметр')

        return self.cleaned_data