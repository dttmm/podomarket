from django.shortcuts import get_object_or_404, render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User
from .forms import PostCreateForm, PostUpdateForm, ProfileUpdateForm
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

    def get_queryset(self):
        return Post.objects.filter(is_sold=False).order_by("-dt_created")


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


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    pk_url_kwarg = 'post_id'
    template_name = 'market/post_form.html'

    raise_exception = True

    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})

    def test_func(self, user):
        return self.get_object().author == user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    tmeplate_name = 'market/post_confirm_delete.html'

    raise_exception = True

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        return self.get_object().author == user


class ProfileView(DetailView):
    model = User
    template_name = 'market/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_posts'] = Post.objects.filter(
            author__id=user_id).order_by("-dt_created")[:8]
        return context


class UserPostView(ListView):
    model = Post
    template_name = 'market/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 8

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author__id=user_id).order_by("-dt_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(
            User, id=self.kwargs.get('user_id'))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'market/profile_set_form.html'

    def get_object(self, query=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'market/profile_update_form.html'

    def get_object(self, query=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs=({"user_id": self.request.user.id}))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    def get_success_url(self):
        return reverse('profile', kwargs=({"user_id": self.request.user.id}))
