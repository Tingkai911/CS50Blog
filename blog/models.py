from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

DEFAULT_ID = 1

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_ID)

    likes = models.ManyToManyField(User, related_name="blog_post_likes")
    dislikes = models.ManyToManyField(User, related_name="blog_post_dislikes")

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    # debug purposes
    objects = models.Manager()

    # to redirect users back to the blog when the created a new post successfully
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


# add comments to the blog post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", default=DEFAULT_ID)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", default=DEFAULT_ID)
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
    
    objects = models.Manager()
