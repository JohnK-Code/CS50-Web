#   on Specification (Following) - Section
#
#   Finished the following section and now doing a small amount of css before moving on 
#   Test all sections working before moving on to Pagination
#   *** Still doing CSS before moving on - this is a new comment 
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
