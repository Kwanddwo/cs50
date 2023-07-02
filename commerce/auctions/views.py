from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
    })


def user_view(request, username):
    user = User.objects.get(username=username)
    return render(request, "auctions/user.html", {
        "user": user
    })


def listing(request, listing_index):
    entry = Listing.objects.get(pk=listing_index)
    seller = entry.seller.username

    if entry.have_bid:
        bids = Bid.objects.filter(auction=listing_index)
        bid_count = len(bids)
        highest_bid = max(bids, key=lambda bid: bid.price)
        entry.current_price = highest_bid.price
        entry.current_bidder = highest_bid.bidder
        entry.save()
    else:
        bid_count = 0
        entry.current_bidder = entry.seller

    return render(request, "auctions/listing.html", {
        "listing": entry,
        "seller": seller,
        "bid_count": bid_count
    })

@login_required
def create_listing(request):
    if request.method == "POST":

        form = ListingForm(request.POST)
        if form.is_valid():

            if form.cleaned_data["current_price"] < 0:
                return HttpResponse("Error: Price cannot be negative.")
            
            listing = Listing(
                name=form.cleaned_data["name"],
                seller=request.user,
                current_bidder=request.user,
                description=form.cleaned_data["description"],
                current_price=form.cleaned_data["current_price"],
                imageurl=form.cleaned_data["imageurl"],
            )
            listing.save()
            listing.category.set(form.cleaned_data["category"])

            return HttpResponseRedirect(reverse("listing", args=[listing.pk]))
        
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            "message": "Form data is incorrect!",
            "form": form
        })
    
    form = ListingForm()
    return render(request, "auctions/create_listing.html", {
            "form": form
        })


@login_required
def bid(request, listing_index):
    if request.method == "POST":
        bidder = request.user
        price = int(request.POST["price"])
        auction = Listing.objects.get(pk=listing_index)

        if auction.seller == bidder:
            return HttpResponse("Error: You can't bid on this auction because you posted it")
        
        if price <= auction.current_price:
            return HttpResponse("Error: Your bid is lower than the current bid")
        
        if auction.have_bid == False:
            auction.have_bid = True
            auction.save()

        bid = Bid(bidder=bidder, price=price, auction=auction)
        bid.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_index]))


@login_required
def close(request, listing_index):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_index)
        if listing.seller != request.user:
            return HttpResponse("Error: You cannot close an auction that isn't yours")
        
        listing.winner = listing.current_bidder
        listing.is_closed = True
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_index]))


@login_required
def watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])

        if request.POST["choice"] == "add":
            request.user.watchlist.add(listing)
        else:
            request.user.watchlist.remove(listing)

    return render(request, "auctions/watchlist.html")


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        if request.POST["delete"]:
           comment = Comment.objects.get(pk=request.POST["delete"])
           comment.delete()
           return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
        if not request.POST["text"]:
            return HttpResponse("Error: Comment is empty")
        comment = Comment(listing=listing, text=request.POST["text"], commenter=request.user)
        comment.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


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


@login_required
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
