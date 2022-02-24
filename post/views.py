from datetime import timedelta
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from post.models import Post

from django.views.decorators.cache import cache_page

from django.utils.decorators import method_decorator

from django.core.cache import cache
import django_rq


@method_decorator(cache_page(100), name='dispatch')
class ListPostView(ListView):
    model = Post
    template_name = "post/list.html"
    context_object_name = "posts"


def create_post():
    Post.objects.create(title="Third Post", content="Third Post Content")


class PostView(View):

    def get(self, request, id):
        post = cache.get(f"post{id}")
        print(django_rq.queues.get_queue(
            "default").enqueue_in(timedelta(seconds=10), create_post))

        # django_rq.enqueue(lambda x: print(x), "Hello I am Queue")
        if not post:
            post = get_object_or_404(Post, id=id)
            cache.set(f"post{id}", post, timeout=10)
        return render(request, "post/detail.html", {"post": post})
