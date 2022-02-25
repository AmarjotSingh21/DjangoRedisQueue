from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"id": self.id})


class UrlShort(models.Model):
    url = models.URLField(unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.slug, self.url}"
