#### Figure out current Bid model ####
### USE RELATED NAME TO ACCESS BID FROM LISTINGS MODEL IN SHELL
######################################


from django.contrib.auth.models import AbstractUser
from django.db import models

## Used to get future date
def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)

# AbstractUser provides default fields, such as, username,
# email, password, etc., could maybe add extra fields later
# if required
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    

# Listings model is related to the User model using a foreign
# key using a many to one relaionship
class Listing(models.Model):
    title = models.CharField(max_length=50)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='listings/', default="\listings\default.gif")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")

    def __str__(self):
        return f"{self.title} - User: {self.user}"


class Bid(models.Model):
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="highest_bidder", null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_name")

    def __str__(self):
        return f"Start Price: {self.starting_bid} - Current Bid: {self.current_bid} - Bidder: {self.current_bidder} - Listing: {self.listing}"
    

class Comment(models.Model):
    user_comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
