from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    CATEGORIES = [
        ('0', 'Танки'),
        ('1', 'Хилы'),
        ('2', 'ДД'),
        ('3', 'Торговцы'),
        ('4', 'Гилдмастеры'),
        ('5', 'Квестгиверы'),
        ('6', 'Кузнецы'),
        ('7', 'Кожевники'),
        ('8', 'Зельевары'),
        ('9', 'Мастера заклинаний')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=1, choices=CATEGORIES)
    title = models.CharField(max_length=128)
    content = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}: {self.author}: {self.date_of_creation}: ' \
               f'{self.category}: {self.title}: {self.content[:40]}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=4096)
    approved = models.BooleanField(default=False)
