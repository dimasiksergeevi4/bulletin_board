from django.db import models
from django.contrib.auth.models import User
from .resources import CATEGORY_THEMES, TYPE_POST
from django.urls import reverse
from django.conf import settings
from datetime import datetime


class Author(models.Model):  # наследуемся от класса Model
    name_author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        self.rating = 0
        for comment_rating in Comment.objects.filter(id_users=self.name_author):
            self.rating += comment_rating.rating_comment

        for post_rating in Post.objects.filter(id_authors=Author.objects.get(id_users=self.name_author)):
            self.rating += post_rating.rating_post * 3

            #    for rating_of_comment in Comment.objects.filter(id_post=post_rating.id_post):
            #       self.rating += rating_of_comment.rating_comment
        self.save()

    def __str__(self):
        return f'{self.name_author}'


class Category(models.Model):
    sport = 'SP'
    policy = 'PL'
    formation = 'FM'
    culture = 'CL'
    rest = 'RS'
    other = 'OT'

    name_category = models.CharField(unique=True, max_length=2, choices=CATEGORY_THEMES, default=other)
    subscribers = models.ManyToManyField(User, related_name='categories')
    #sub_user = models.ManyToManyField(User, through='SubscribersUsers')

    def __str__(self):
        return f'Категория: {self.name_category}'

    def get_subscribers_emails(self):
        res = set()
        for user in self.subscribers.all():
            res.add(user.email)
        return res


class Post(models.Model):
    news = 'NW'
    post = 'PS'

    id_authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=2, choices=TYPE_POST)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_post = models.IntegerField(default=0, db_column='rating')

    post_category = models.ManyToManyField(Category, through='PostCategory')

    @property
    def rating(self):
        return self.rating_post

    @rating.setter
    def rating(self, value):
        self.rating_post = value if value >= 0 and isinstance(value, int) else 0
        self.save()

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f'Заголовок: {self.title[:10]}.\n  Текст: {self.text}.\n  Дата загрузки: {self.time_in}'

    def get_absolute_url(self):
        return reverse('new', args=[str(self.id)])


class PostCategory(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #sub_user = models.ManyToManyField(User, through='SubscribersUsers')

    def __str__(self):
        return f'Статья: {self.id_post}. | Категория: {self.id_category}.'

    #@property
    #def get_subscribers_emails(self):
    #    res = set()
    #    for user in self.subscribers.all():
    #        res.add(user.email)
    #    return res


#class SubscribersUsers(models.Model):
 #   id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 #   categories = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    id_users = models.ForeignKey(User, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0, db_column='rating')

    @property
    def rating(self):
        return self.rating_comment

    @rating.setter
    def rating(self, value):
        self.rating_comment = value if value >= 0 and isinstance(value, int) else 0
        self.save()

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


class Appointment(models.Model):
    date = models.DateField(default=datetime.utcnow)
    user_name = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f'{self.user_name}: {self.message}'
