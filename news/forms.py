from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
                 'object_title',
                 'object_content',
                 'author',
                 'post_type',
                 'category',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        object_content = cleaned_data.get("object_content")
        object_title = cleaned_data.get("object_title")

        if object_content is not None and len(object_content) < 20:
            raise ValidationError({
                "object_content": "Content"
            })

        if object_title == object_content:
            raise ValidationError(
                "Content must not be same as Title"
            )

        return cleaned_data