from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .forms import PostForm

# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'market/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    ordering = ['-dt_created']


class PostDetailView(DetailView):
    model = Post
    template_name = 'market/post_detail.html'
    pk_url_kwarg = 'post_id'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'market/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        return reverse('index')
