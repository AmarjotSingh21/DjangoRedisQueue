from django.urls import path
from post.views import ListPostView, PostView

app_name = "post"

urlpatterns = [
    path('', ListPostView.as_view(), name="list"),
    path('posts/<int:id>/detail/', PostView.as_view(), name="detail"),
]
