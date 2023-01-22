from django.db import models

#importing embeded video field from homePage/templates/homePage/home.html
from embed_video.fields import EmbedVideoField

#embeded video class model
class Video(models.Model):
    title = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    url = EmbedVideoField()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-added']


