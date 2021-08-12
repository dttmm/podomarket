from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostCreateForm, PostUpdateForm
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from .funtions import confirmation_required_redirect

# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'market/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    ordering = ['-dt_created']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'market/post_detail.html'
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'market/post_form.html'

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostUpdateForm
    pk_url_kwarg = 'post_id'
    template_name = 'market/post_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    tmeplate_name = 'market/post_confirm_delete.html'

    def get_success_url(self):
        return reverse('index')


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        return reverse('index')
