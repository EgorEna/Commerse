from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        'categories': Category.objects.all()
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required(login_url='auctions:login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='auctions:login')
def create(request):
    if request.method == "POST":
        new_listing = Listing(
            title=request.POST['title'],
            owner=request.user,
            description=request.POST['description'],
            image=request.POST['image'],
            price=request.POST['starting_bid'],
        )
        if request.POST['category'] != 'No category':
            category = Category.objects.get(pk=request.POST['category'])
            new_listing.category = category
        new_listing.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/create.html", {
        'categories': Category.objects.all()
    })


@login_required(login_url='auctions:login')
def detail(request, listing_id: int, dictionary=None):
    dictionary = dictionary or {}
    listing = Listing.objects.get(pk=listing_id)
    last_bid_member = None
    bids = listing.bids.all()
    comments = listing.comments.all()
    if bids:
        last_bid_member = listing.bids.last().member.username
    default = {
        'listing': listing,
        'owner': listing.owner == request.user,
        'bids': listing.bids.count(),
        'active': listing.active,
        'last_bid_member': last_bid_member,
        'comments': comments,
        'categories': Category.objects.all()
    }
    if request.user.is_authenticated:
        res = {**default, **dictionary}
        return render(request, "auctions/detail.html", res)
    else:
        return render(request, "auctions/detail.html", default)


@login_required(login_url='auctions:login')
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        'categories': Category.objects.all()
    })


@login_required(login_url='auctions:login')
def add(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    if listing in request.user.watchlist.all():
        dictionary = {
            'message': {
                'type': 'error',
                'message': 'Already added to watchlist',
            }
        }
        return detail(request, listing_id, dictionary=dictionary)
    request.user.watchlist.add(listing)
    dictionary = {
        'message': {
            'type': 'succes',
            'message': 'Succesfully added',
        }
    }
    return detail(request, listing_id, dictionary=dictionary)


@login_required(login_url='auctions:login')
def remove(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist_view.remove_view(listing)
    return HttpResponseRedirect(reverse("auctions:watchlist"))


@login_required(login_url='auctions:login')
def bid(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    price = listing.price
    if int(request.POST['bid']) > price:
        new_bid = Bid(member=request.user, listing=listing)
        new_bid.save()
        listing.price = request.POST['bid']
        listing.save()
        return HttpResponseRedirect(reverse('auctions:detail', args=(listing_id,)))
    else:
        dictionary = {
            'error_bid': 'Your bid is smaller than current',
        }
        return detail(request, listing_id, dictionary=dictionary)


@login_required(login_url='auctions:login')
def close(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return detail(request, listing_id)


@login_required(login_url='auctions:login')
def comment(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    content = request.POST['content']
    comment = Comment(
        listing=listing,
        content=content,
        creater=request.user
    )
    comment.save()
    return HttpResponseRedirect(reverse('auctions:detail', args=(listing_id,)))


@login_required(login_url='auctions:login')
def delete_comment(request, listing_id: int, comment_id: int):
    Comment.objects.get(pk=comment_id).delete()
    return HttpResponseRedirect(reverse('auctions:detail', args=(listing_id,)))


def category(request, category_name: str):
    category = Category.objects.get(name=category_name)
    return render(request, 'auctions/category.html', {
        "listings": Listing.objects.filter(category=category),
        'categories': Category.objects.all(),
        'category': category,
    })
