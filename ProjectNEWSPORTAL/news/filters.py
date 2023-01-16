from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
         'object_title': ['icontains'],
         'post_type': ['icontains'],
         'time_created': []
        }
