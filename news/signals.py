from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
#from ProjectNEWSPORTAL import settings
from django.conf import settings
from .models import PostCategory, Category, Post

#from project.settings import SITE_URL, DEFAULT_FROM_EMAIL


def send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subcribers: list[str] = []
        for category in categories:
            subcribers += category.subscribers.all()

        subcribers = [s.email for s in subcribers]

        send_notification(instance.preview(), instance.pk, instance.title, subcribers)
