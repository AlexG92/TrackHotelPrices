import urllib2
import re
import csv
from datetime import datetime, timedelta

def main():
    dates_and_prices = []
    for week in xrange(0,52):
        ## Date that you want the app to start searching from
        start_date = '10252014'

        ## How many nights you want to stay
        length_of_stay = 5

        start_datetime = datetime.strptime(start_date,'%m%d%Y') + timedelta(days=week*7)
        end_date = start_datetime + timedelta(days=length_of_stay)
        start_date_formatted = '%s/%s/%s' % (str(start_datetime.month).zfill(2), str(start_datetime.day).zfill(2), str(start_datetime.year).zfill(2))
        end_date_formatted = '%s/%s/%s' % (str(end_date.month).zfill(2), str(end_date.day).zfill(2), str(end_date.year).zfill(2))
        ## URL Example
        ## http://www.expedia.com/Cancun-Hotels-Hyatt-Zilara-Cancun-All-Inclusive.h1635542.Hotel-Information?packagePIID=3224b148-d62b-417a-ad91-cf4aca7b7d29-7&usePS=1&packageType=fh&hotelId=1635542&currentRatePlan=200813448204083154&packageType=fh&originId=6000346&ftla=LAX&numberOfRooms=1&ttla=CUN&toDate=01/21/2015&hlrId=0&fromDate=01/16/2015&defaultFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&destinationId=179995&adultsPerRoom[1]=2&currentFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&inttkn=nKfb3NEw7HnUlG25
        #url = 'http://www.expedia.com/Cancun-Hotels-Hyatt-Zilara-Cancun-All-Inclusive.h1635542.Hotel-Information?packagePIID=3224b148-d62b-417a-ad91-cf4aca7b7d29-7&usePS=1&packageType=fh&hotelId=1635542&currentRatePlan=200813448204083154&packageType=fh&originId=6000346&ftla=LAX&numberOfRooms=1&ttla=CUN&toDate=' + end_date_formatted + '&hlrId=0&fromDate=' + start_date_formatted + '&defaultFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&destinationId=179995&adultsPerRoom[1]=2&currentFlights=5329f4bb76ed9b599412732cc751a0c7,c0c578ec810a513d23c2147140a1c89e&inttkn=nKfb3NEw7HnUlG25'
        url = 'http://www.expedia.com/Cancun-Hotels-Finest-Playa-Mujeres-By-Excellence-Group-All-Inclusive.h8673168.Hotel-Information?packagePIID=446a23f0-ae78-42af-a3e0-bf0d8b6b2aa8-20&usePS=1&packageType=fh&hotelId=8673168&currentRatePlan=200734900203669685&originId=6000346&ftla=LAX&numberOfRooms=1&ttla=CUN&toDate=' + end_date_formatted + '&hlrId=0&fromDate=' + start_date_formatted + '&defaultFlights=5e8687aa484100057ae50e7e01f21cb6,6c876d819fae6915ad55987e16a31be8&destinationId=179995&adultsPerRoom[1]=2&currentFlights=5e8687aa484100057ae50e7e01f21cb6,6c876d819fae6915ad55987e16a31be8&inttkn=EoOwoNAeqiNLqF13'
        
        price = get_price(url)

        ## In case price comes back as None
        if price:
            dates_and_prices.append([start_date_formatted, price])

    write_to_csv(dates_and_prices)

def get_price(url, retries=0):
    """
    Get the price from the expedia page.
    Sometimes the expedia page craps out, so recursive
    calls until it comes back until above a certain limit.

    @Params | retries = number of retries, self passed.
    @Params | url = url to search the price for
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
    except urllib2.HTTPError:
        print '404'
        print url


def write_to_csv(write_this):
    with open('G:\_work\TrackHotelPrices\dates.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(write_this)


if __name__ == "__main__":
    main()