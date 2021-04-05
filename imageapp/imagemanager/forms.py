from django import forms

from imagemanager.models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('url', 'image')
        exclude = ('resized_image',)

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
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    class Meta:
        model = Image
        fields = ('width', 'height')

    def clean(self):
        self.cleaned_data = super().clean()

        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if not width and not height:
            raise forms.ValidationError('Необходимо указать хотя бы один параметр')

        return self.cleaned_data