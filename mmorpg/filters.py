from django_filters import *
import django_filters
from .models import Comment, Post
from django import forms


class CommentFilter(FilterSet):
    post = django_filters.ChoiceFilter(choices=None, label="Сообщение:", empty_label="Все сообщения")

    creation = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                         label="Создано позднее, чем ", lookup_expr='date__gt')
    approved = django_filters.ChoiceFilter(choices=[('0', 'Нет'), ('1', 'Да')], label="Согласован:",
                                           lookup_expr='iexact', empty_label="Не важно")

    class Meta:
        model = Comment
        fields = {
            'post',
            'date_of_creation',
            'approved'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs['request']
        my_choices = lambda: [(p.id, f'{p.id} - {p.title} - {p.date_of_creation.strftime("%d-%m-%Y %H:%M")}')
                                 for p in Post.objects.filter(author=request.user).order_by('-date_of_creation')]
        self.filters['post'].extra.update({'choices': my_choices})

