from django.shortcuts import render
from .functions import listingsPerPage, soldListingsPerPage, getHemnetUrls
from django.contrib import messages
import json
from .kommunURLs import listedURL, soldURL

# Create your views here.


def home_page(request):

    if request.method == "POST":

        # for sale
        # current_listings_url = "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744"

        # Final prices
        # sold_listings_url = "https://www.hemnet.se/salda/bostader?item_types=bostadsratt&location_ids=17744"

        kommun = request.POST.get('kommun')
        print(kommun)
        listings = []
        dataType = {'type': None}
        if request.POST.get('category') == "listed" and kommun != '':
            for key, value in listedURL.items():
                if key == kommun:
                    current_listings_url = value
            # paginator index it should be different for sold page and current listings page
            page_index = -2
            urls = getHemnetUrls(current_listings_url, page_index)
            page_number = 0
            for url in urls:
                page_number += 1
                print(f"Fatching page #{page_number}")
                listings += listingsPerPage(url)
            message1 = "Currently there are"
            message2 = f"listings in {kommun} kommun."
            dataType['type'] = 'listed'

        elif request.POST.get('category') == "sold" and kommun != '':
            for key, value in soldURL.items():
                if key == kommun:
                    sold_listings_url = value
            # paginator index it should be different for sold page and current listings page
            page_index = -1
            urls = getHemnetUrls(sold_listings_url, page_index)
            page_number = 0
            for url in urls:
                page_number += 1
                print(f"Fatching page #{page_number}")
                listings += soldListingsPerPage(url)
            message1 = "Total of"
            message2 = f"final prices found in {kommun} kommun."
            dataType['type'] = 'sold'
        else:
            messages.success(
                request, 'Please choose between "Currently listed" and "Final prices" as well as the kommun.')
            context = {}
            return render(request, "home.html", context)

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
                       'kommun': f"{kommun} kommun",
                       'dataType': json.dumps(dataType),
                       }
        else:
            context = {}
    else:
        context = {}
    return render(request, "home.html", context)
