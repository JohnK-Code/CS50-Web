from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import datetime, os

# advert categories
Modern = "Modern"
Classic = "Classic"
American = "American"
categories = (
    (Modern, "Modern"),
    (Classic, "Classic"),
    (American, "American")
)

# function used to change filename - used as callback for ImageField 
def rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join('upload/', filename)

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
# if required - AbstractUser is provided by Django 
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

# model used to store Listing date who created it
class Listing(models.Model):
    category = models.CharField(choices=categories, max_length=64)
    title = models.CharField(max_length=100)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to=rename, blank=True) # uses callback function to rename image file before being saved to database
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    startingBid = models.DecimalField(max_digits=10, decimal_places=0)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(default=return_date_time())
    active = models.BooleanField(default=True)
    watchListUser = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"Advert: {self.title}"

# model used to store Bid data and who placed it 
class Bid(models.Model):
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="bid_listing")
    currentBid = models.DecimalField(max_digits=10, decimal_places=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

    def __str__(self):
        return f"{self.listing}, Bidder: {self.bidder}, Bid: £{self.currentBid}"
    

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    commentTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.comment}, User: {self.user}, {self.listing}"
    
