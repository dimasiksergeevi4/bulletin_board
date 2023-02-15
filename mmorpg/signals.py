from datetime import *
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Comment, User
from django.db.models import F
from .tasks import send_email_to_author

@receiver(post_save, sender=Comment)
def inc_created_posts(sender, instance, created, **kwargs):
    send_email_to_author.apply_async([instance.user.username, instance.post.id, instance.text], countdown=5)
