from django.urls import reverse_lazy
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Appointment
from django.core.mail import send_mail


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        # context['New post is coming soon'] = None
        context['is_not_authors'] = not self.request.user.groups.filter(name='author').exists()
        context['user_auth'] = self.request.user.is_authenticated
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        is_subscribers = True
        for cat in post.post_category.all():
            if self.request.user not in cat.subscribers.all():
                is_subscribers = False
        context['is_subscribers'] = is_subscribers
        return context


class PostCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель постов
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'
    permission_required = ('post.add_post')

    def form_valid(self, form):
        post_in = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/news/create/':
                post_in.type_of_post = 'NW'
            elif path_info == '/news/article/create/':
                post_in.type_of_post = 'PS'
        post_in.save()
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class PostUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.change_post')


# Представление удаляющее товар.
class PostDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
    permission_required = ('post.delete_post')


@login_required
def subscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=pk)
    category = post.name_category.all()
    for cat in category:
        if user not in cat.sub_user.all():
            cat.sub_user.add(user)
    return redirect('/news/')


@login_required
def unsubscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=pk)
    category = post.post_category.all()
    for cat in category:
        if user in cat.sub_user.all():
            cat.sub_user.remove(user)
    return redirect('/news/')


class CategoryListView(ListView):
    model = Post
    template_name = 'categories_list.html'
    context_object_name = 'categories_new_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписаны.'
    return render(request, 'subscribe.html', {'category': category, 'message': message})




class AppointmentView(View):
    template_name = 'appointment_created.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'appointment_created.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            user_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.user_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя пользователя и дата будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием
            from_email='Sender2023@yandex.ru',  # здесь указываете почту, с которой будете отправлять
            recipient_list=[]  # здесь список получателей.
        )

        return redirect('appointments:appointment_create')
