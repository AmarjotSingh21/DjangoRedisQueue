from django.db import models
from django.urls import reverse


class UrlShort(models.Model):
    url = models.URLField(unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.slug, self.url}"
