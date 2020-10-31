from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django import forms 
from datetime import *
from .models import *

class NewListingFor(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    image = forms.URLField()
    starting_bid = forms.IntegerField(label='Starting Bid',min_value=5)

def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = NewListingFor(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            new_listing = Listing(
                owner=user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.POST['image'],
                price=request.POST['starting_bid']
            )
            new_listing.save()
            user.listings.add(new_listing)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/create.html",{
                "form": NewListingFor(request.POST),
                "message": "Incorrectly entered data, make sure you entered everything correctly."
            })
    return render (request,"auctions/create.html",{
        "form":NewListingFor()
    })

def detail(request,listing_id,dictionary={}):
    listing = Listing.objects.get(pk=listing_id)
    current_bid = None
    bids = listing.bids.all()
    if bids:
        current_bid = listing.bids.last()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        default = {
            'listing':listing,
            'is_owner':listing.owner == user,
            'bids': listing.bids.count(),
            'current_bid':current_bid.member if current_bid.member.username != request.user.username else 'You',
        }
        res = {**default,**dictionary}
        return render(request,"auctions/detail.html",res)
    else:
        return render(request,"auctions/detail.html",{
            'listing':listing,
            'bids':listing.bids.count(),
        })

def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings,
    })

def add(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_bid = None
    bids = listing.bids.all()
    if bids:
        current_bid = listing.bids.last()
    if listing in request.user.watchlist.all():
        dictionary = {
            'message': {
            'type':'error',
            'message':'Already added to watchlist',
            }
        }
        return detail(request,listing_id,dictionary=dictionary)
    request.user.watchlist.add(listing)
    dictionary = { 
           'message': {
            'type':'succes',
            'message': 'Succesfully added',
        }
    }
    return detail(request,listing_id,dictionary=dictionary)

def remove(request,listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        raise Http404("You're not authenticated for such action")

def bid(request,listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        price = listing.price
        if int(request.POST['bid']) > price:
            new_bid = Bid(member=request.user,listing=listing)
            new_bid.save()
            listing.price = request.POST['bid']
            listing.save()
            return HttpResponseRedirect(reverse('detail',args=(listing_id,)))
        else:
            dictionary = {
                'error_bid':'Your bid is smaller than current',
            }
            return detail(request,listing_id,dictionary=dictionary)
    else:
        raise Http404("You're not authenticated for such action")