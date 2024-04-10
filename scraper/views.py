from django.shortcuts import render
from .functions import listingsPerPage, soldListingsPerPage, getHemnetUrls
from django.contrib import messages
import json

# Create your views here.


def home_page(request):

    if request.method == "POST":

        # for sale
        current_listings_url = "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744"

        # Final prices
        sold_listings_url = "https://www.hemnet.se/salda/bostader?item_types=bostadsratt&location_ids=17744"

        if request.POST.get('category') == "listed":
            # url = current_listings_url
            listings = []
            # paginator index it should be different for sold page and current listings page
            page_index = -2
            urls = getHemnetUrls(current_listings_url, page_index)
            i = 0
            for url in urls:
                i += 1
                print(f"Fatching page #{i}")
                listings += listingsPerPage(url)
            message1 = "Currently there are"
            message2 = "listings in Stockholm area."
        elif request.POST.get('category') == "sold":
            # url = sold_listings_url
            listings = []
            # paginator index it should be different for sold page and current listings page
            page_index = -1
            urls = getHemnetUrls(sold_listings_url, page_index)
            i = 0
            for url in urls:
                i += 1
                print(f"Fatching page #{i}")
                listings += soldListingsPerPage(url)
            message1 = "Total of"
            message2 = "final prices found."
        else:
            messages.success(
                request, 'Please choose between "Currently listed" and "Final prices"')
            context = {}
            return render(request, "home.html", context)
        # filter = FilteringSettings()

        # filter.address = request.POST['address']
        # filter.maxfee = request.POST['maxfee']
        # filter.minrooms = request.POST['minrooms']
        # filter.maxrooms = request.POST['maxrooms']
        # filter.minarea = request.POST['minarea']
        # filter.maxarea = request.POST['maxarea']
        # listings = listingsPerPage(url, filter)

        # urls = getHemnetUrls()
        # print(f"{len(urls)} urls found")
        # listings = []
        # for url in urls:
        #    listings += listingsPerPage(url)

        total = 0
        numberOfListings = len(listings)
        print(f"{numberOfListings} listings found")
        listings_dictionary = []
        if len(listings) >= 1:
            for listing in listings:
                # if some items have no price ignore them for calculatin of avg
                if listing.price != None:
                    total += listing.price
                else:
                    numberOfListings -= 1

                # Convert the listings into dictionary to input to json file
                listings_dictionary.append(listing.__dict__)

            averagePrice = total/numberOfListings

            context = {'message': f"{message1} {str(numberOfListings)} {message2}",
                       'listings': json.dumps(listings_dictionary, indent=2),
                       }
        else:
            context = {}
    else:
        context = {}
    return render(request, "home.html", context)
