from django.contrib.auth.models import AbstractUser
from django.db import models

from django.urls import reverse


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name='watchers')


class Listing(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='listings', blank=True, null=True)

    title = models.CharField(max_length=64)
    image = models.URLField(blank=True)
    description = models.TextField()
    price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('auctions:detail', args=[str(self.id)])


class Bid(models.Model):
    member = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids')

    def get_absolute_url(self):
        return reverse('auctions:detail', args=[str(self.listing.id)])


class Comment(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')
    creater = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')

    content = models.TextField(blank=False)

    def get_absolute_url(self):
        return reverse('auctions:detail', args=[str(self.listing.id)])


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
