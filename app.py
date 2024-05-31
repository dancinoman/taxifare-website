import requests
import streamlit as st
import datetime
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy
import math

'''
# Taxi Fare Calculator in NY city
'''
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# Start form on sidebar
with st.sidebar:
    with st.form('Taxi form'):
        pickup_date = st.date_input('Enter your date pickup', value=datetime.datetime(2014,1,6, 10, 10))
        pickup_time = st.time_input('Enter time pickup', value=datetime.datetime(2014,1,6, 10, 10))

        try:
            adress_pickup = st.text_input("Adress to pickup", "200 Broadway")
            adress_dropoff = st.text_input("Adress to drop off", "Queens, NY 11430")

            geolocator_pick = Nominatim(user_agent="Taxi Map")
            geocode = RateLimiter(geolocator_pick.geocode, min_delay_seconds=1)
            location1 = geolocator_pick.geocode(f"{adress_pickup} NYC")
            location2 = geolocator_pick.geocode(f"{adress_dropoff} NYC")

            lat_pick = location1.latitude
            lon_pick = location1.longitude

            lat_drop = location2.latitude
            lon_drop = location2.longitude

            map_data = pd.DataFrame({'lat': [lat_pick], 'lon': [lon_pick]})



        except:

            st.error('Adress not valid. Please try another adress.')

        passenger_count = st.number_input(min_value= 1, max_value= 8, step= 1, label= 'Number of passenger')
        submitted = st.form_submit_button('CALCULATE')




st.map(map_data)

if submitted:

    url = 'https://taxifare.lewagon.ai/predict'


    info = {
        'pickup_datetime' : f'{pickup_date} {pickup_time}' ,
        'pickup_longitude' : lon_pick,
        'pickup_latitude' : lat_pick,
        'dropoff_longitude' : lon_drop,
        'dropoff_latitude' : lat_drop,
        'passenger_count' : passenger_count

    }

    response = requests.get(url, params= info)
    json = response.json()


    st.html(

        f"""
        <H1>
    <span style="background-color:blue">
        Only {round(json['fare'], 2)} $
    </span>
    </H1>
        """

    )
