from django.urls import path

from post.views import TopNewsStories, GetNewsDetail

app_name = "post"

urlpatterns = [
    path('top_stories/<int:x>/', TopNewsStories.as_view(), name="list"),
    path('<str:slug>/', GetNewsDetail.as_view(), name="detail"),

]
