# fix image upload problem - file not saving in images folder
# try change file name on upload so no images have same name :-)
# check bookmark for help - not sure if it's any good, didn't get anytime to read it

from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import datetime, os

# used to create random image file name
def rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


# used to get range for car year
YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

# used to get current date plus 7 days
def return_date_time():
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=7)

# model used to store User data 
# AbstractUser provides default fields, such as, username,
# email, password, etc., could maybe add extra fields later
# if required
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

# model used to store Listing date who created it
class Listing(models.Model):
    category = models.CharField(max_length=64)
    title = models.CharField(max_length=100)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='upload/', blank=True) # provides location to upload file for model and also allows it to be blank if required
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(default=return_date_time())
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Advert: {self.title}"

# model used to store Bid data and who placed it 
class Bid(models.Model):
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="bid_listing")
    currentBid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

    def __str__(self):
        return f"{self.listing}, Bidder: {self.bidder}, Bid: £{self.currentBid}"
    

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")

    def __str__(self):
        return f"Comment: {self.comment}, User: {self.user}, {self.listing}"
    

class WatchList(models.Model):
    onWatchList = models.BooleanField(default=True)
    lisitng = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watch_list_listing")
    watchUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_list_user")

    def __str__(self):
        return f"{self.lisitng}, Watched: {self.onWatchList}, Watcher: {self.watchUser}"
    