import string
from django.shortcuts import redirect, render
from django.views.generic import View

from django.views.generic import View
from django.http import JsonResponse

import requests

from post.models import UrlShort
import random
import django_rq


def create_url_short(url_short_list: list):
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

        # async url shortening
        django_rq.get_queue("default").enqueue(create_url_short, url_shorts)

        return render(request, "urlshort/list.html", {"posts": posts})


class GetNewsDetail(View):
    def get(self, request, slug: str) -> JsonResponse:
        try:
            url = UrlShort.objects.get(slug=slug).url
        except UrlShort.DoesNotExist:
            return JsonResponse({"msg": "Not Found!"})

        return redirect(url)
