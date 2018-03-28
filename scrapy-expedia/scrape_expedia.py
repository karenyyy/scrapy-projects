import json
import requests
from lxml import html
import argparse
import pymongo
import lxml

def parse(source, destination, date):
    for i in range(5):
        try:
            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(
                source, destination, date)
            print url
            response = requests.get(url, verify=False)
            parser = html.fromstring(response.text)
            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
            flight_data = json.loads(raw_json["content"])
            # print (flight_data)
            with open('raw.json', 'w') as fp:
                json.dump(flight_data, fp, indent=4)

            lists = []

            try:
                for i in flight_data['legs'].keys():
                    total_distance = flight_data['legs'][i].get("formattedDistance", '')
                    exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')

                    departure_location_city = flight_data['legs'][i].get('departureLocation', {}).get('airportCity', '')
                    arrival_location_city = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCity', '')
                    airline_name = flight_data['legs'][i].get('carrierSummary', {}).get('airlineName', '')

                    no_of_stops = flight_data['legs'][i].get("stops", "")
                    flight_duration = flight_data['legs'][i].get('duration', {})
                    flight_hour = flight_duration.get('hours', '')
                    flight_minutes = flight_duration.get('minutes', '')
                    flight_days = flight_duration.get('numOfDays', '')

                    if no_of_stops == 0:
                        stop = "Nonstop"
                    else:
                        stop = str(no_of_stops) + ' Stop'

                    total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour,
                                                                                    flight_minutes)
                    departure = departure_location_city
                    arrival = arrival_location_city
                    carrier = flight_data['legs'][i].get('timeline', [])[0].get('carrier', {})
                    plane = carrier.get('plane', '')
                    plane_code = carrier.get('planeCode', '')
                    formatted_price = "{0:.2f}".format(exact_price)

                    if not airline_name:
                        airline_name = carrier.get('operatedBy', '')

                    timings = []
                    for timeline in flight_data['legs'][i].get('timeline', {}):
                        if 'departureAirport' in timeline.keys():
                            departure_airport = timeline['departureAirport'].get('longName', '')
                            departure_time = timeline['departureTime'].get('time', '')
                            arrival_airport = timeline.get('arrivalAirport', {}).get('longName', '')
                            arrival_time = timeline.get('arrivalTime', {}).get('time', '')
                            flight_timing = {
                                'departure_airport': departure_airport,
                                'departure_time': departure_time,
                                'arrival_airport': arrival_airport,
                                'arrival_time': arrival_time
                            }
                            timings.append(flight_timing)

                    flight_info = {'stops': stop,
                                   'ticket price': formatted_price,
                                   'departure': departure,
                                   'arrival': arrival,
                                   'flight duration': total_flight_duration,
                                   'airline': airline_name,
                                   'plane': plane,
                                   'timings': timings,
                                   'plane code': plane_code
                                   }
                    lists.append(flight_info)
            except IndexError:
                return
            sortedlist = sorted(lists, key=lambda k: k['ticket price'], reverse=False)
            return sortedlist

        except ValueError:
            print ("Retrying...")

        return "failed to process the page"


if __name__ == "__main__":

    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('source', help='Source airport code')
    # argparser.add_argument('destination', help='Destination airport code')
    # argparser.add_argument('date', help='MM/DD/YYYY')
    #
    # args = argparser.parse_args()
    # source = args.source
    # destination = args.destination
    # date = args.date

    airport_list = []
    with open('airport_code.json', 'r') as f:
        airport = json.load(f)
        for i in range(3, len(airport) - 1):
            for j in range(i + 1, len(airport)):
                if airport[i] == 'nyc' and airport[j] == 'mia':
                    continue
                else:
                    airport_list.append([airport[i], airport[j]])
    for source, destination in airport_list:
        for year in range(2018, 2019):
            for month in range(4,13):
                for day in range(1, 31):
                    date = '{}/{}/{}'.format(month, day, year)
                    print ("Fetching flight details")
                    try:
                        scraped_data = parse(source, destination, date)
                        # with open('%s-%s-%s-%s-%s.json' % (source, destination, month, day, year), 'w') as fp:
                        #     json.dump(scraped_data, fp, indent=4)
                        if scraped_data == "failed to process the page":
                            continue
                        mng_client = pymongo.MongoClient('localhost', 27017)
                        mng_db = mng_client['vevo']  # Replace mongo db name
                        collection_name = 'expedia_flight'  # Replace mongo db collection name
                        db_cm = mng_db[collection_name]
                        db_cm.insert(scraped_data)
                    except lxml.etree.XMLSyntaxError:
                        continue
                    except IndexError:
                        continue
                    except TypeError:
                        continue
                    except pymongo.errors.InvalidOperation:
                        continue
