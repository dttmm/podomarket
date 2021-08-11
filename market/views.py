from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import ListView
from .models import Post

# Create your views here.


def index(request):
    return render(request, 'market/index.html')


class IndexView(ListView):
    model = Post
    template_name = 'market/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    ordering = ['-dt_created']


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        return reverse('index')
