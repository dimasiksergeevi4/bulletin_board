from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .models import Post, Comment
from datetime import date, timedelta
from django.db.models import Q


@shared_task
def send_email_to_author(user, post_id, text):
    to_send = User.objects.filter(username=Post.objects.get(id=post_id).author).values('first_name', 'last_name',
                                                                                       'username', 'email')
    title = f'Новый комментарий {text[:50]} на ваше объявление!'
    html_content = render_to_string(
        'post_created.html',
        {
            'title': title,
            'text': text,
            'cur_user': user,
            'url': f'http://127.0.0.1:8000/post/{post_id}/',
            'user': f"{to_send[0]['first_name']} {to_send[0]['last_name']} ({to_send[0]['username']})"
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body=text[:50],
        from_email='semenyak7@yandex.ru',
        to=[to_send[0]['email']],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_email_by_approved(user, post_id, text):
    post_data = Post.objects.filter(id=post_id).values('id', 'title', 'content', 'author')
    author_name = User.objects.get(id=post_data[0]['author'])
    to_send = User.objects.filter(username=user).values('first_name', 'last_name', 'username', 'email')
    title = post_data[0]['title']
    html_content = render_to_string(
        'comment_approved.html',
        {
            'title': title,
            'content': post_data[0]['content'],
            'text': text,
            'author': author_name,
            'url': f'http://127.0.0.1:8000/post/{post_data[0]["id"]}/',
            'user': f"{to_send[0]['first_name']} {to_send[0]['last_name']} ({to_send[0]['username']})"
        }
    )
    msg = EmailMultiAlternatives(
        subject='Ваш комментарий был принят автором объявления',
        body=text[:50],
        from_email='semenya7@yandex.ru',
        to=[to_send[0]['email']],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def inform_for_new_posts():
    print('Дайджест начал работу')
    date_from = date.today() - timedelta(days=8)
    date_to = date.today() - timedelta(days=1)
    users = User.objects.all().values('first_name', 'last_name', 'username', 'email')

    post_source = Post.objects.filter(Q(date_of_creation__gte=date_from) & Q(date_of_creation__lt=date_to))
    comment_source = Comment.objects.filter(Q(date_of_creation__gte=date_from) & Q(date_of_creation__lt=date_to))

    title = f'Дайджест новых объявлений и комментариев'

    for i in range(users.count()):
        user_name = f"{users[i]['first_name']} {users[i]['last_name']} ({users[i]['username']})"
        html_content = render_to_string(
                'post_digest.html',
                {
                    'date_from': date_from,
                    'date_to': date_to,
                    'title': title,
                    'user': user_name,
                    'posts': post_source,
                    'comments': comment_source,
                    'url_start': 'http://127.0.0.1:8000/',
                }
            )
        msg = EmailMultiAlternatives(
                subject=title,
                body=f'Дайджест новых постов с {date_from} по {date_to}.',
                from_email='semenyak7@yandex.ru',
                to=[users[i]['email']],
            )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    print('Рассылка дайджеста завершена')
