from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.FloatField()
    imageurl = models.URLField(blank=True)
    category = models.ManyToManyField(AuctionCategory, blank=True, related_name="listings")
    have_bid = models.BooleanField(default=False)
    current_bidder = models.ForeignKey(User, on_delete=models.PROTECT, related_name="highest_bids", blank=True)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} for ${self.current_price} by {self.seller}"
    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField()
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.bidder} bid {self.price} on {self.auction}"

class Comment(models.Model):
    pass