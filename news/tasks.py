from datetime import date, timedelta
from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ProjectNEWSPORTAL import settings
from .models import Post, Category, User


@shared_task
def last_post_week():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = Category.objects.filter(name_catagory__in=categories).values_list('subscribers__email', flat=True)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='За предыдущую неделю в категории вышли новые статьи',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


#@shared_task
#def send_email(pk_, id_cat):
#    post = Post.objects.get(id=pk_)
#    emails = User.objects.filter(category__id__in=id_cat).values('email').distinct()
#    emails_list = [item['email'] for item in emails]
#    html_content = render_to_string(
#        'daily_post.html',
#        {
#            'Post': post
#        }
#    )
#
#    msg = EmailMultiAlternatives(
#        subject=f'{post.title}',
#        from_email=settings.DEFAULT_FROM_EMAIL,
#        to=emails_list
#    )
#
#    msg.attach_alternative(html_content, 'text/html')
#    msg.send()


@shared_task
def notify_about_new_post_when_create(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subcribers: list[str] = []
        for category in categories:
            subcribers += category.subscribers.all()

        subcribers = [s.email for s in subcribers]

        for x in subcribers:
            html_content = render_to_string(
                'post_created_email.html',
                {
                    'text': instance.preview(),
                    'link': f'{settings.SITE_URL}/news/{instance.pk}',
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=x,
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()
