
from bs4 import BeautifulSoup
import requests
import re
from .myClasses import Listing, FilteringSettings

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}


def getHemnetUrls(url):
    """ final prices
          "https://www.hemnet.se/salda/bostader?item_types=bostadsratt&location_ids=17744&page=50"
    url = "https://www.hemnet.se/salda/bostader?item_types=bostadsratt&location_ids=17744"
    """
    # url = "https://www.hemnet.se/salda/bostader?item_types=bostadsratt&location_ids=17744"

    """ For sale currently
    url = "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744"

    """

    urls = [url]

    html_text = requests.get(url, headers=headers).text
    base_soup = BeautifulSoup(html_text, 'lxml')

    # getting the number of pages in pagination
    paginator = base_soup.find_all(
        'a', class_='hcl-button hcl-button--secondary')
    number_of_pages = int(paginator[-2].text)

    # creating urls for each pagination, starting from 1 because the 21 page is providded above, it is the "url"
    for i in range(2, number_of_pages+1):
        urls.append(
            f'{url}&page={i}')
        # f'https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744&page={i}') the link for appartments ofr sale
    print(len(urls))
    return urls


def extractprice(attribute):
    string = attribute.text.replace("\xa0", "")
    digits = re.search(r'\d+', string)
    digitsGrouped = digits.group()
    return int(digitsGrouped)


def extractNumbers(attribute):
    string = attribute.text.replace("\xa0", "")
    numerical_part = re.search(r'[\d,]+', string).group()
    number = numerical_part.replace(',', '.')
    if '.' in str(number):
        return float(number)
    else:
        return int(number)


def listingsPerPage(url, filter=None):

    pageListings = []

    html_page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    listings = soup.find_all(
        'div', class_='hcl-grid hcl-grid--columns-1 hcl-grid--md-columns-2')

    for listing in listings[5:]:
        currentListing = Listing()
        address = listing.find(
            'div', class_='Location_address___eOo4').text
        currentListing.address = address
        attributes = listing.find_all(
            'div', class_='hcl-grid__item ForSaleAttributes_item__GT4Ro')

        for attribute in attributes:
            if 'kr/m²' in attribute.text:
                pass
            elif 'kr/mån' in attribute.text:
                monthlyFee = attribute.text
                currentListing.monthlyFee = extractprice(attribute)

            elif 'kr' in attribute.text:
                price = extractprice(attribute)
                if price > 100000:
                    currentListing.price = price

            elif 'm²' in attribute.text and 'kr' not in attribute.text:
                area = attribute.text
                currentListing.area = extractNumbers(attribute)

            elif 'rum' in attribute.text:
                numberOfRooms = attribute.text
                currentListing.roomNumber = extractNumbers(attribute)

            elif 'vån' in attribute.text:
                floor = re.search(r"[\d/]+", attribute.text).group()
                currentListing.floor = floor
        if filter != None:
            filter_results = filterListings(currentListing, filter)
            if filter_results != None:
                pageListings.append(filter_results)
        elif currentListing.price != None:
            pageListings.append(currentListing)

    return pageListings
    # print(currentListing)


def filterListings(listing: Listing, filter: FilteringSettings):
    if filter.address == None:
        pass
    elif filter.address in listing.address:
        pass
    else:
        return None

    if filter.maxfee == None:
        pass
    elif listing.monthlyFee <= filter.maxfee:
        pass
    else:
        return None

    if filter.minarea == None:
        pass
    elif listing.area >= filter.minarea:
        pass
    else:
        return None

    if filter.maxarea == None:
        pass
    elif listing.area <= filter.maxarea:
        pass
    else:
        return None

    if filter.minrooms == None:
        pass
    elif listing.roomNumber >= filter.minrooms:
        pass
    else:
        return None

    if filter.maxrooms == None:
        pass
    elif listing.roomNumber <= filter.maxrooms:
        pass
    else:
        return None

    return listing


# def filterListings(listing, address=None, maxfee=None, minrooms=None, maxrooms=None, minarea=None, maxarea=None):
#     filter=FilteringSettings(address, maxfee, minrooms, maxrooms, minarea, maxarea)


def soldListingsPerPage(url, filter=None):

    pageListings = []

    html_page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    listings = soup.find_all(
        'div', class_='hcl-grid hcl-grid--columns-1 hcl-grid--md-columns-2')

    for listing in listings:
        currentListing = Listing()

        address = listing.find(
            'div', class_='Location_address___eOo4').text
        currentListing.address = address

        attributes = listing.find_all(
            'div', class_='hcl-flex--container hcl-flex--gap-2 hcl-flex--justify-space-between hcl-flex--md-justify-flex-start')

        currentListing.monthlyFee = extractprice(
            attributes[0].find('span', class_='hcl-text'))
        area_and_rooms = attributes[0].find_all(
            'p', class_='hcl-text hcl-text--medium')
        for item in area_and_rooms:
            if 'm²' in item.text:
                currentListing.area = extractNumbers(item)
            elif 'rum' in item.text:
                currentListing.roomNumber = extractNumbers(item)

        currentListing.price = extractprice(attributes[1])

        if filter != None:
            filter_results = filterListings(currentListing, filter)
            if filter_results != None:
                pageListings.append(filter_results)
        elif currentListing.price != None:
            pageListings.append(currentListing)
            print(currentListing)

    return pageListings
