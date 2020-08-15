from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    theme = models.CharField(max_length=5, default='light')

    def __str__(self):
        return f'{self.user.username} Profile'

    # debug purposes
    objects = models.Manager()
