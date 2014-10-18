import urllib2
import re
import csv
from datetime import datetime

URLS = {
    'alex_second': 'http://www.expedia.com/Cancun-Hotels-Finest-Playa-Mujeres-By-Excellence-Group-All-Inclusive.h8673168.Hotel-Information?ajaxRequestType=airchangeview&packagePIID=4ea69f2f-869e-4c17-91cf-37d565242cfd-0&outboundTimeFilters=1432710900000,1432795500000,1432739400000,1432831680000&packageType=fh&packageType=2&pqtp=3236.44&curc=USD&hotelId=8673168&hlrId=0&reorderFiltersTreatment=0&defaultFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&totalResultsCount=154&originId=6000346&ftla=LAX&numberOfRooms=1&ttla=CUN&toDate=06/01/2015&isDirectFlight=0&hashTag=picturesAndTours&returnTimeFilters=1433140200000,1433200320000,1433171820000,1433229180000&usePS=0&dest=179995&fromDate=05/27/2015&destinationId=179995&adultsPerRoom[1]=2&returnToRD=1&part=0&currentRatePlan=200739401203670430&currentFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&inttkn=kpKkISQgO0Re4Fbx',
    'ani':'http://www.expedia.com/Cancun-Hotels-Hyatt-Zilara-Cancun-All-Inclusive.h1635542.Hotel-Information?packagePIID=3224b148-d62b-417a-ad91-cf4aca7b7d29-7&usePS=1&packageType=fh&hotelId=1635542&currentRatePlan=200813448204083154&packageType=fh&originId=6000346&ftla=LAX&numberOfRooms=1&ttla=CUN&toDate=06/01/2015&hlrId=0&fromDate=05/27/2015&defaultFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&destinationId=179995&adultsPerRoom[1]=2&currentFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&inttkn=nKfb3NEw7HnUlG25'
}

def main():
    for url in URLS:
        price = get_price(URLS[url])

        ## In case price comes back as None
        if price:
            write_to_csv(url, price)

def get_price(url, retries=0):
    """
    Get the price from the expedia page.
    Sometimes the expedia page craps out, so recursive
    calls until it comes back until above a certain limit.

    @Params | retries = number of retries, self passed.
    """
    findprice = '<span id="totalPrice">(.*)</span>'

    if retries > 10: return
    try:
        htmlpage = urllib2.urlopen(url).read()
        price = re.findall(findprice, htmlpage)[0]
        int_price = float(price.replace('$','').replace(',',''))
        return int_price
    except IndexError:
        retries += 1
        return get_price(url, retries)


def write_to_csv(url, price):
    with open('G:\_work\TrackHotelPrices\data.csv', 'ab') as csvfile:
        date = datetime.now()
        date_formatted = '%s/%s/%s' % (date.month, date.day, date.year)
        writer = csv.writer(csvfile)
        writer.writerow((date_formatted, price, url))


if __name__ == "__main__":
    main()