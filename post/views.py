from datetime import timedelta
import string
from time import sleep
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from post.models import Post

from django.views.decorators.cache import cache_page

from django.utils.decorators import method_decorator

from django.core.cache import cache
# import django_

from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import redirect

import requests

from post.models import UrlShort
import random
import django_rq


def create_url_short(url_short_list: list):
    UrlShort.objects.create(url=random.choice(
        string.ascii_lowercase), slug=random.choice(string.ascii_lowercase))
    sleep(5)
    UrlShort.objects.bulk_create(url_short_list)


class TopNewsStories(View):

    def get(self, request, x: int) -> JsonResponse:
        res = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json").json()

        if type(res) is not list:
            return JsonResponse({"msg": "Error!"})

        post_ids = res[:x]
        posts = []

        url_shorts = []

        for post_id in post_ids:
            url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
            res = requests.get(url).json()

            slug = "".join([random.choice(string.ascii_lowercase)
                           for _ in range(5)])
            try:
                url_short = UrlShort.objects.get(url=url)
            except UrlShort.DoesNotExist:
                url_short = UrlShort(url=url, slug=slug)
                url_shorts.append(url_short)

            posts.append({
                "id": post_id,
                "title": res["title"],
                "url": "http://localhost:8000/" + url_short.slug,
            })
        django_rq.get_queue("default").enqueue(create_url_short, url_shorts)

        return JsonResponse(posts, safe=False)


class GetNewsDetail(View):
    def get(self, request, slug: str) -> JsonResponse:
        print(slug)
        try:
            url = UrlShort.objects.get(slug=slug).url
        except UrlShort.DoesNotExist:
            return JsonResponse({"msg": "Not Found!"})

        return redirect(url)


# @method_decorator(cache_page(100), name='dispatch')
# class ListPostView(ListView):
#     model = Post
#     template_name = "post/list.html"
#     context_object_name = "posts"


# def create_post():
#     Post.objects.create(title="Third Post", content="Third Post Content")


# class PostView(View):

#     def get(self, request, id):
#         post = cache.get(f"post{id}")
#         print(django_rq.queues.get_queue(
#             "default").enqueue_in(timedelta(seconds=10), create_post))

#         # django_rq.enqueue(lambda x: print(x), "Hello I am Queue")
#         if not post:
#             post = get_object_or_404(Post, id=id)
#             cache.set(f"post{id}", post, timeout=10)
#         return render(request, "post/detail.html", {"post": post})
