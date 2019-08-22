#!/usr/bin/python
from pyowm import OWM
import json
import urllib2
import elasticsearch
import pprint
import time
import geocoder
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import googlemaps
import datetime

maps_api_key = 'ENTER KEY HERE' # https://developers.google.com/maps/documentation/maps-static/intro
owm_api_key = 'ENTER KEY HERE' # https://openweathermap.org/api
spot_feed_id = 'ENTER FEED ID HERE' # https://faq.findmespot.com/index.php?action=showEntry&data=69

try:
    es = elasticsearch.Elasticsearch(["localhost"],port=9200,http_auth=("elastic","changeme"))
    gmaps = googlemaps.Client(key=maps_api_key)
    owm = OWM(owm_api_key)
except:
    print "unable to load owm, es or gmaps"

mapping = {
    "mappings" : {
            "doc" : {
                "properties" : {
                        "tracker_id" : { "type" : "keyword"},
                        "tracker_name" : { "type" : "keyword"},
                        "tracker_description" : { "type" : "keyword"},
                        "tracker_status" : { "type" : "keyword"},
                        "tracker_usage" : { "type" : "long"},
                        "tracker_daysRange" : { "type" : "long"},
                        "tracker_detailedMessageShown" : { "type" : "keyword"},
                        "tracker_type" : { "type" : "keyword"},
                        "clientUnixTime" : { "type" : "long"},
                        "id" : { "type" : "long"},
                        "messengerId" : { "type" : "keyword"},
                        "messengerName" : { "type" : "keyword"},
                        "messageContent" : { "type" : "keyword"},
                        "messageType" : { "type" : "keyword"},
                        "unixTime" : { "type" : "long"},
                        "modelId" : { "type" : "keyword"},
                        "showCustomMsg" : { "type" : "keyword"},
                        "dateTime" : { "type" : "date"},
                        "messageDetail" : { "type" : "keyword"},
                        "batteryState" : { "type" : "keyword"},
                        "hidden" : { "type" : "long"},
                        "altitude" : {"type" : "long"},
                        "weather_clouds" : { "type" : "long" },
                        "weather_rain"   : {
                            "properties" : {
                                "3h": {"type": "long"}
                                }
                        },
                        "weather_snow"   : {
                            "properties" : {
                                "3h": {"type": "long"}
                                }
                        },
                        "weather_wind" : {
                            "properties" : {
                                "speed" : {"type":"float"},
                                "gust" : {"type":"float"},
                                "deg" : {"type":"long"}
                                }
                        },
                        "weather_wind_direction" : { "type" : "keyword"},
                        "weather_humidity" : {"type":"long"},
                        "weather_pressure" : {
                            "properties" : {
                                "press" : {"type":"long"},
                                "sea_level" : {"type": "text"}
                                }
                        },
                        "weather_temperature" : {
                            "properties" : {
                                "temp": {"type":"float"},
                                "temp_kf": {"type":"float"},
                                "temp_max": {"type":"float"},
                                "temp_min": {"type":"float"}
                            }
                        },
                        "weather_short_description" : {"type":"keyword"},
                        "weather_long_description" : {"type":"text"},
                        "weather_place" : {"type":"keyword"},
                        "weather_sunrise" : {
                            "type" : "date",
                            "format" : "yyyy-MM-dd'T'HH:mm:ssZ"
                            },
                        "weather_sunset" : {
                            "type" : "date",
                            "format" : "yyyy-MM-dd'T'HH:mm:ssZ"
                            },
                        "weather_timestamp" : {
                            "type" : "date",
                            "format" : "yyyy-MM-dd'T'HH:mm:ssZ"
                            },
                        "location" : {"type":"geo_point"},
                        "previous_location" : {"type":"geo_point"},
                        "origin_distance_miles" : {"type":"float"},
                        "origin_distance_text" : {"type":"keyword"},
                        "origin_distance_meters" : {"type":"float"},
                        "origin_estimated_duration_seconds" : {"type":"float"},
                        "origin_estimated_duration_text" : {"type":"keyword"},
                        "distance_miles" : {"type":"float"},
                        "distance_text" : {"type":"keyword"},
                        "estimated_duration_seconds" : {"type":"float"},
                        "estimated_duration_text" : {"type":"keyword"},
                        "distance_meters" : {"type":"float"},
                        "address_raw" : {"type":"text"},
                        "address_city" : { "type" : "keyword"},
                        "address_house_number" : { "type" : "keyword"},
                        "address_country" : { "type" : "keyword"},
                        "address_county" : { "type" : "keyword"},
                        "address_state" : { "type" : "keyword"},
                        "address_road" : { "type" : "keyword"},
                        "address_country_code" : { "type" : "keyword"},
                        "address_neighbourhood" : { "type" : "keyword"},
                        "address_postcode" : { "type" : "keyword"},
                        "elevation_meters" : {"type":"float"},
                        "elevation_feet" : {"type":"float"},
                        "elevation_resolution" : {"type":"float"},
                        "latitude" : {"type":"float"},
                        "longitude" : {"type":"float"}
                }
            }
    }
}
es.indices.create(index="mike_location",body=mapping, ignore=400)

print "----------------------------------------"
print datetime.datetime.now()
print "----------------------------------------"

try:
    tracker = json.load(urllib2.urlopen("https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/{0}/message.json".format(spot_feed_id)))
    tracker_data = tracker["response"]["feedMessageResponse"]["feed"]
    message_data = tracker["response"]["feedMessageResponse"]["messages"]["message"][0]
    previous_message_data = tracker["response"]["feedMessageResponse"]["messages"]["message"][1]
except:
    print "unable to load tracker data"

if es.exists(index="mike_location", doc_type="_doc", id=message_data["id"]) == False:
    print "doc does not exist"
    doc = {}
    doc["tracker_id"] = tracker_data["id"]
    doc["tracker_name"] = tracker_data["name"]
    doc["tracker_description"] = tracker_data["description"]
    doc["tracker_status"] = tracker_data["status"]
    doc["tracker_usage"] = tracker_data["usage"]
    doc["tracker_daysRange"] = tracker_data["daysRange"]
    doc["tracker_detailedMessageShown"] = tracker_data["detailedMessageShown"]
    doc["tracker_type"] = tracker_data["type"]
    doc["clientUnixTime"] = message_data["@clientUnixTime"]
    doc["id"] = message_data["id"]
    doc["messengerId"] = message_data["messengerId"]
    doc["messengerName"] = message_data["messengerName"]
    try:
        doc["messageContent"] = message_data["messageContent"]
    except:
        print "no message content"
    doc["messageType"] = message_data["messageType"]
    doc["unixTime"] = message_data["unixTime"]
    doc["latitude"] = message_data["latitude"]
    doc["longitude"] = message_data["longitude"]
    doc["location"] = { "lat": message_data["latitude"], "lon": message_data["longitude"] }
    doc["previous_location"] = { "lat": previous_message_data["latitude"], "lon": previous_message_data["longitude"] }
    doc["modelId"] = message_data["modelId"]
    doc["showCustomMsg"] = message_data["showCustomMsg"]
    doc["dateTime"] = message_data["dateTime"]
    doc["messageDetail"] = message_data["messageDetail"]
    doc["batteryState"] = message_data["batteryState"]
    doc["hidden"] = message_data["hidden"]
    doc["altitude"] = message_data["altitude"]

    try:
        current_location = "{0},{1}".format(str(message_data["latitude"]), str(message_data["longitude"]))
        previous_location = "{0},{1}".format(str(previous_message_data["latitude"]), str(previous_message_data["longitude"]))

        origin_distance_result = gmaps.distance_matrix("32.5898145,-116.4691323",current_location,mode="walking",units="imperial")
        doc["origin_distance_miles"] = origin_distance_result["rows"][0]["elements"][0]["distance"]["value"] * 0.00062137
        doc["origin_distance_text"] = origin_distance_result["rows"][0]["elements"][0]["distance"]["text"]
        doc["origin_distance_meters"] = origin_distance_result["rows"][0]["elements"][0]["distance"]["value"]
        doc["origin_estimated_duration_text"] = origin_distance_result["rows"][0]["elements"][0]["duration"]["text"]
        doc["origin_estimated_duration_seconds"] = origin_distance_result["rows"][0]["elements"][0]["duration"]["value"]

        distance_result = gmaps.distance_matrix(previous_location,current_location,mode="walking",units="imperial")
        doc["distance_miles"] = distance_result["rows"][0]["elements"][0]["distance"]["value"] * 0.00062137
        doc["distance_text"] = distance_result["rows"][0]["elements"][0]["distance"]["text"]
        doc["distance_meters"] = distance_result["rows"][0]["elements"][0]["distance"]["value"]
        doc["estimated_duration_seconds"] = distance_result["rows"][0]["elements"][0]["duration"]["value"]
        doc["estimated_duration_text"] = distance_result["rows"][0]["elements"][0]["duration"]["text"]

    except:
        print "unable to calculate distance"

    try:
        geolocator = Nominatim()
        location_address = geolocator.reverse((message_data["latitude"], message_data["longitude"]))
        location_raw = location_address.raw['address']
        doc["address_raw"] = location_address.address
        try:
            doc["address_city"] = location_raw['city']
        except:
            print "unable to get city"
        try:
            doc["address_house_number"] = location_raw['house_number']
        except:
            print "unable to get address number"
        try:
            doc["address_country"] = location_raw['country']
        except:
            print "unable to get country"
        try:
            doc["address_county"] = location_raw['county']
        except:
            print "unable to get county"
        try:
            doc["address_state"] = location_raw['state']
        except:
            print "unable to get state"
        try:
            doc["address_road"] = location_raw['road']
        except:
            print "unable to get road"
        try:
            doc["address_country_code"] = location_raw['country_code']
        except:
            print "unable to get country code"
        try:
            doc["address_neighbourhood"] = location_raw['neighbourhood']
        except:
            print "unable to get neighbourhood"
        try:
            doc["address_postcode"] = location_raw['postcode']
        except:
            print "unable to get postcode"
    except:
        print "unable to reverse lookup coordinates"

    try:
        elevation_result = gmaps.elevation((message_data["latitude"], message_data["longitude"]))
        doc["elevation_meters"] = elevation_result[0]['elevation']
        doc["elevation_resolution"] = elevation_result[0]['resolution']
        doc["elevation_feet"] = doc["elevation_meters"] * 3.28084
    except:
        print "unable to calculate elevation"

    try:
        obs = owm.weather_at_coords(message_data["latitude"], message_data["longitude"])
        location = obs.get_location()
        weather = obs.get_weather()
    except:
        print "unable to get weather data"

    doc["weather_clouds"] = weather.get_clouds()
    doc["weather_rain"] = weather.get_rain()
    doc["weather_snow"] = weather.get_snow()
    doc["weather_wind"] = weather.get_wind()

    degrees = weather.get_wind()["deg"]
    if degrees < 23 or degrees >= 338:
        doc["weather_wind_direction"] = 'N'
    elif degrees < 68:
        doc["weather_wind_direction"] = 'NE'
    elif degrees < 113:
        doc["weather_wind_direction"] = 'E'
    elif degrees < 158:
        doc["weather_wind_direction"] = 'SE'
    elif degrees < 203:
        doc["weather_wind_direction"] = 'S'
    elif degrees < 248:
        doc["weather_wind_direction"] = 'SW'
    elif degrees < 293:
        doc["weather_wind_direction"] = 'W'
    elif degrees < 338:
        doc["weather_wind_direction"] = 'NW'

    doc["weather_humidity"] = weather.get_humidity()
    doc["weather_pressure"] = weather.get_pressure()
    doc["weather_temperature"] = weather.get_temperature(unit="fahrenheit")
    doc["weather_short_description"] = weather.get_status()
    doc["weather_long_description"] = weather.get_detailed_status()
    doc["weather_place"] = location.get_name()
    doc["weather_sunrise"] = weather.get_sunrise_time('iso').replace(' ','T')
    doc["weather_sunset"] = weather.get_sunset_time('iso').replace(' ','T')
    doc['weather_timestamp'] = weather.get_reference_time(timeformat='iso').replace(' ','T')

    if(doc["dateTime"]>= doc["weather_sunrise"] and doc["dateTime"] <= doc["weather_sunset"]):
        doc['day_or_night'] = "Day"
    else:
        doc['day_or_night'] = "Night"

    try:
        es.index(index="mike_location", doc_type="_doc", id=doc["id"], body=doc)
        pprint.pprint(doc)
    except:
        print "unable to index in elasticsearch"
else:
    print "doc already exists"
print "----------------------------------------"
