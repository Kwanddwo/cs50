from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.TextField()
    imageurl = models.URLField(blank=True)
    price = models.FloatField()
    category = models.ManyToManyField(AuctionCategory, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.name}: {self.price}$"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass