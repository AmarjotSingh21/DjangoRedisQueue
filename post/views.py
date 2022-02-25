from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from post.models import Post


class ListPostView(ListView):
    model = Post
    template_name = "post/list.html"
    context_object_name = "posts"


class PostView(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, "post/detail.html", {"post": post})
