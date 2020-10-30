from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing',related_name='watchers')

class Listing(models.Model):
    owner = models.ForeignKey('User',on_delete=models.CASCADE,related_name='listings')
    title = models.CharField(max_length=64)
    image = models.URLField(blank=True)
    description = models.TextField()
    bid = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Bid():    
    pass

class Comment():
    content = models.ForeignKey('Listing',on_delete=models.CASCADE,related_name='commets')
