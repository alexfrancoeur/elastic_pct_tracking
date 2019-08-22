### SPOT Tracking with the Elastic Stack

In 2018, my brother was hiking the Pacific Crest Trail. After much convincing, we were able to get him to purchase a SPOT. Luckily, this had an API associated with it and I was able to track his movements throughout his hike. I blogged about this experience in the links below. There seems to be some general interest in this code so I figured it couldn't hurt to throw it on GitHub.

* [Hiking the Pacific Crest Trail with the Elastic Stack](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack)
* [Hiking the Pacific Crest Trail with the Elastic Stack - Part 2: Hitting 1000](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack-part-2-hitting-1000)
* [Hiking the Pacific Crest Trail with the Elastic Stack - Part 3: Mission Complete](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack-part-3-mission-complete)

I am hosting a read only instance on [Elastic Cloud](https://www.elastic.co/products/elasticsearch/service) that takes advantage of freely available features like [Maps](https://www.elastic.co/products/maps) and [Canvas](https://www.elastic.co/what-is/kibana-canvas).

* Host: `https://b778b00c9167a18a95c2a263f6baea62.us-east-1.aws.found.io:9243`
* Username: `Elastic_PCT`
* Password: `whereismike`

### Setup

I haven't had time to generalize the script or saved objects for Kibana. I had a cron job that ran the python script every 10 minutes. You'll want to open the `mike_location.py` and add a Google Maps API key, an OpenWeatherMap API, SPOT feed ID and the details for your cluster. If you make no changes to the index name, you can import the `saved_objects.ndjson` file. Unfortunately, everything will be labeled "Mike" .

_This is a no judgement coding zone, I was and still am a python n00b. I also realize it's unnecessary to create the index and mappings every run. If you want to improve this code, feel free to submit a PR :-)_

You can run the stack on [Elastic Cloud](https://www.elastic.co/products/elasticsearch/service) or [download](https://www.elastic.co/downloads/) for a self managed experience.

### Dashboard

Click [here](https://b778b00c9167a18a95c2a263f6baea62.us-east-1.aws.found.io:9243/s/pacific-crest-trail/app/kibana#/dashboard/f0119530-c451-11e9-9263-973275f93f5b) and login with `Elastic_PCT : whereismike` for a read only view of the latest dashboard

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/dashboard.png)

### Canvas

Click [here](https://b778b00c9167a18a95c2a263f6baea62.us-east-1.aws.found.io:9243/s/pacific-crest-trail/app/canvas#/workpad/workpad-e720a1b1-2522-445c-9f7a-0027ee57b4dd/page/1) and login with `Elastic_PCT : whereismike` for a read only view of this Canvas workpad

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/canvas1.png)

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/canvas2.png)

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/canvas3.png)


### Elastic Maps

Click [here](https://b778b00c9167a18a95c2a263f6baea62.us-east-1.aws.found.io:9243/s/pacific-crest-trail/app/maps#/map/2ba52ae0-c460-11e9-9263-973275f93f5b) and login with `Elastic_PCT : whereismike` for a read only view of this map

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/maps1.png)

![screenshot](https://github.com/alexfrancoeur/elastic_pct_tracking/blob/master/images/maps2.png)

### Example document

```json
{
  "_index": "mike_location-v2",
  "_type": "doc",
  "_id": "1077296819",
  "_version": 1,
  "_score": null,
  "_source": {
    "distance_text": "36 ft",
    "origin_distance_miles": 1363.81270176,
    "weather_place": "Marietta-Alderwood",
    "origin_estimated_duration_text": "18 days 21 hours",
    "weather_rain": {
      "1h": 0.25
    },
    "weather_wind": {
      "speed": 1.22,
      "deg": 140.001
    },
    "messageType": "TRACK",
    "day_or_night": "Night",
    "showCustomMsg": "N",
    "weather_wind_direction": "SE",
    "weather_long_description": "light rain",
    "weather_sunset": "2018-10-07T01:38:12+00",
    "batteryState": "LOW",
    "address_state": "Washington",
    "address_postcode": "98226-8048",
    "tracker_detailedMessageShown": false,
    "address_country": "USA",
    "id": 1077296819,
    "elevation_feet": 168.13703008712767,
    "origin_distance_text": "1,364 mi",
    "tracker_status": "ACTIVE",
    "address_raw": "I 5, Birchwood, Whatcom County, Washington, 98226-8048, USA",
    "weather_timestamp": "2018-10-06T00:35:00+00",
    "altitude": 74,
    "address_road": "I 5",
    "weather_short_description": "Rain",
    "location": {
      "lat": 48.79611,
      "lon": -122.52904
    },
    "previous_location": {
      "lat": 48.79602,
      "lon": -122.52913
    },
    "weather_sunrise": "2018-10-06T14:17:14+00",
    "latitude": 48.79611,
    "distance_meters": 11,
    "hidden": 0,
    "origin_distance_meters": 2194848,
    "weather_humidity": 76,
    "weather_snow": {},
    "modelId": "SPOT3",
    "tracker_daysRange": 7,
    "distance_miles": 0.00683507,
    "weather_clouds": 90,
    "elevation_resolution": 4.771975994110107,
    "address_county": "Whatcom County",
    "tracker_id": "0xUCMqoO8VBNO2qCuh8MMobhyCmrlAYbR",
    "messengerId": "0-3086869",
    "tracker_usage": 0,
    "tracker_name": "Mike's SPOT",
    "origin_estimated_duration_seconds": 1632078,
    "clientUnixTime": "0",
    "messageDetail": "",
    "address_country_code": "us",
    "estimated_duration_seconds": 8,
    "weather_pressure": {
      "press": 1014,
      "sea_level": null
    },
    "unixTime": 1538787465,
    "elevation_meters": 51.24816513061523,
    "tracker_type": "SHARED_PAGE",
    "longitude": -122.52904,
    "dateTime": "2018-10-06T00:57:45+0000",
    "messengerName": "Mike's Spot",
    "weather_temperature": {
      "temp_max": 53.96,
      "temp_kf": null,
      "temp": 52.95,
      "temp_min": 51.8
    },
    "tracker_description": "Mike's SPOT",
    "estimated_duration_text": "1 min"
  },
  "fields": {
    "dateTime": [
      "2018-10-06T00:57:45.000Z"
    ],
    "weather_sunset": [
      "2018-10-07T01:38:12.000Z"
    ],
    "weather_timestamp": [
      "2018-10-06T00:35:00.000Z"
    ],
    "hour_of_day": [
      0
    ],
    "weather_sunrise": [
      "2018-10-06T14:17:14.000Z"
    ]
  },
  "sort": [
    1538787465000
  ]
}
```
