from django.shortcuts import render
from .functions import listingsPerPage
from .myClasses import FilteringSettings


# Create your views here.


def home_page(request):
    url = "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744"
    # listings = listingsPerPage(url)

    # total = 0

    # for listing in listings:
    #     total += listing.price
    # avg = total/len(listings)

    # context = {'price': int(avg),
    #            'listings': len(listings)}
    # return render(request, "home.html", {context})

    if request.method == "POST":
        filter = FilteringSettings()

        filter.address = request.POST['address']
        filter.maxfee = request.POST['maxfee']
        filter.minrooms = request.POST['minrooms']
        filter.maxrooms = request.POST['maxrooms']
        filter.minarea = request.POST['minarea']
        filter.maxarea = request.POST['maxarea']

        listings = listingsPerPage(url, filter)
        total = 0
        if len(listings) >= 1:
            for listing in listings:
                if listing.price != None:
                    total += listing.price
            avg = total/len(listings)
            context = {'price': int(avg),
                       'listings_length': len(listings),
                       'listings': listings
                       }
        else:
            context = {}
    else:
        context = {}
    return render(request, "home.html", context)
