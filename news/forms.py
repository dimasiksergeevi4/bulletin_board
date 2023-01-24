from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'id_authors',
            'title',
            'text',
            'post_category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data
