from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 275 or img.width > 275:
    #         size_tuple = (275, 275)
    #         img.thumbnail(size_tuple)
    #         img.save(self.image.path)

    def image_url(self):
        try:
            image = self.image.url
        except:
            image = ""
        return image
