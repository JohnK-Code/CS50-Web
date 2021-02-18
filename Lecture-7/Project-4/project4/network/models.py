#   on Specification (Following) - Section
#
#
#   On edit post section now - need to figure out how to GET tweet data and how to POST the tweet data.
#   Check AJAX bookmark to GET & POST data.
#   
#   Maybe try see if React or another javacsript library can allow me to add an edit form to a post when edit clicked.
#   React hidden element via class may help ***
#
#
#   Take time doing each section seperatly and don't rush 

from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import datetime, os

# function used to rename image file and save it in the upload folder
def rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join('upload/', filename)


class User(AbstractUser):
    picture = models.ImageField(upload_to=rename, blank=True)

    def delete(self, *args, **kwargs):
        self.picture.delete()
        super().delete(*args, **kwargs)


class Post(models.Model):
    content = models.CharField(max_length=140)
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
