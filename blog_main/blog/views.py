from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Post, Category, Tag


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostCreate(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    model = Post
    #fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user_is_staff

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    #fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/update_post.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if (current_user.is_authenticated and current_user == self.get_object().author) or current_user.is_superuser:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def categories_posts(request, slug):
    if slug=='no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category = category)

    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
        'post_list': post_list
    }

    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = Post.objects.filter(tags = tag)

    context = {
        'tags': Tag.objects.all(),
        'tag': tag,
        'post_list': post_list
    }

    return render(request, 'blog/post_list.html', context)
