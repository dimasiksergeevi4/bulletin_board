from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from .tasks import send_email_by_approved
from .filters import CommentFilter
from .forms import UserForm, PostForm, CommentForm

def to_dict(obj):
    opts = obj._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(obj)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(obj)]
    return data


@login_required
def approve_comment(request, *args, **kwargs):
    Comment.objects.filter(id=kwargs['pk']).update(approved=True)
    comment = Comment.objects.get(id=kwargs['pk'])
    send_email_by_approved.apply_async([comment.user.username, comment.post.id, comment.text], countdown=5)
    return redirect(request.META.get('HTTP_REFERER'))


class PostList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user

        comment_list = []
        for obj in context['post_list']:
            obj = to_dict(obj)

            if Comment.objects.order_by('-date_of_creation').filter(post=obj['id']).exists():
                obj['last_comment'] = Comment.objects.order_by('-date_of_creation').filter(post=obj['id'])[0].text
                obj['last_comment_author'] = Comment.objects.order_by('-date_of_creation').filter(post=obj['id'])[0].user
            else:
                obj['last_comment'] = 'Пока нет комментариев'

            obj['category'] = [_[1] for _ in Post.CATEGORIES if _[0] == obj['category']][0]
            obj['to_edit'] = True if self.request.user.is_authenticated and obj['author'] == \
                                     self.request.user.id else False
            obj['to_comment'] = True if self.request.user.is_authenticated and obj['author'] != \
                                        self.request.user.id else False
            obj['author'] = User.objects.get(id=obj['author']).username

            comment_list.append(obj)

        context['post_list'] = comment_list
        return context


class CommentListFiltered(LoginRequiredMixin, ListView):
    model = Comment
    ordering = '-date_of_creation'
    template_name = 'comment_list.html'
    context_object_name = 'comment_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user

        return context

    def get_queryset(self):
        queryset = Comment.objects.order_by('-date_of_creation').filter(post__in=Post.objects.filter(author=self.request.user))
        print(self.request.GET)
        self.filterset = CommentFilter(self.request.GET, queryset, request=self.request)
        return self.filterset.qs


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user_edit.html'

    def form_valid(self, form):
        self.success_url = '/user/'
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) \
            if self.get_object().id == request.user.id else HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context


class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'one_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        context['comments'] = Comment.objects.order_by('-date_of_creation').filter(post=self.object.id)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) \
            if self.get_object().author == request.user else HttpResponse(status=403)


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(id=self.request.path.split('/')[-3])
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        context['commented_post'] = f"{Post.objects.get(id=self.request.path.split('/')[-3]).title} " \
                                    f"автора {Post.objects.get(id=self.request.path.split('/')[-3]).author}"
        return context


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy('comment_search')
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy('post_list')
        return super().form_valid(form)
