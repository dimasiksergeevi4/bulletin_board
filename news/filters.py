#from django_filters import FilterSet, ModelMultipleChoiceFilter
#from .models import Post, Author
#
#
#class PostFilter(FilterSet):
#   class Meta:
#       model = Post
#       fields = {
#           'title': Post.objects.all(),
#           'id_authors': Author.objects.filter(name_author=),
#           'time_in': [
#               'lt',  # цена должна быть меньше или равна указанной
#               'gt',  # цена должна быть больше или равна указанной
#           ],
#       }
#
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author
from django import forms

class PostFilter(FilterSet):
    #time_in__gt = DateFilter(field_name='time_in', label='Start date', widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='date__gte')
    #
    #class Meta:
    #    model = Post
    #    fields = {
    #        'title': ['icontains'],
    #        'id_authors': ['exact'],
    #    }

    search_title = CharFilter(
        field_name='title',
        label='Название статьи',
        lookup_expr='icontains',
        #empty_label='Все заголовки',
        #queryset=Post.objects.all(),
    )
    search_author = ModelChoiceFilter(
        empty_label='Все авторы',
        field_name='id_authors',
        label='Автор',
        queryset=Author.objects.all(),
    )
    post_date__gt = DateFilter(
        field_name='time_in',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte'
    )

