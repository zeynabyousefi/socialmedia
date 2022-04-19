from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.contrib import messages
from .models import PostUser
from .forms import CreatePost, CreateComment


class PostView(View):
    template = 'post/posts.html'

    def get(self, request):
        post = PostUser.objects.all()
        return render(request, self.template, {"post": post})


class PostDetail(View):
    template = 'post/detail.html'
    form_class = CreateComment

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(PostUser, pk=kwargs['post_id'], slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, slug):
        post = PostUser.objects.get(pk=post_id, slug=slug)
        comment = post.post_comment.all()
        return render(request, self.template, {'post': post, 'comment': comment, 'forms': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "create a new post", 'success')
            return redirect('post_detail', new_comment.post.id, new_comment.post.slug)


class PostRecently(View):
    template = 'home/home.html'

    def get(self, request):
        posts = PostUser.objects.get_query_set().all().order_by('-created')

        return render(request, self.template, {'posts': posts})


class PostCreate(LoginRequiredMixin, View):
    form_class = CreatePost
    template = 'post/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, "create a new post", 'success')
            return redirect('post_detail', new_post.id, new_post.slug)
        # print(form.errors)


class PostDelete(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = PostUser.objects.get(pk=post_id)

        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "delete was successfully", 'success')
        else:
            messages.error(request, "you can't delete", 'danger')
        return redirect('home')


class Update(LoginRequiredMixin, View):
    form_class = CreatePost
    template = 'post/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = PostUser.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you can not edit', 'danger')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.save()
            messages.success(request, "updated post", 'success')
            return redirect('post_detail', new_post.id, new_post.slug)
