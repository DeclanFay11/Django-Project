import datetime
import time
import re
import csv
import json
from datetime import datetime
from hashlib import sha256

from selenium import webdriver
from seleniumwire import webdriver as wire_driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import requests
from requests.utils import requote_uri
from shapely.geometry import Point, Polygon
import brotli

GPS_REGEX = '\-?\d{1,3}\.\d{1,8}'
CONTAINER_FORMAT = '\w{4}[0-9]{7}'


def marinetraffic_vessels_in_port(port_name=None, port_code=None):

    data = None
    data_url_pat = '.*reports\?asset\_type.*' 

    if port_code:

        options = wire_driver.ChromeOptions()
        options.add_argument('headless')
        
        default_fields = [  'shipname',
                            'recognized_next_port',
                            'reported_eta',
                            'arrived',
                            'dwt',
                            'imo',
                            'mmsi',
                            'lat_of_latest_position',
                            'lon_of_latest_position',
                            'current_port',
                            'reported_destination',
                            'draught',
                            'current_port_unlocode',
                            'navigational_status',
                            'year_of_build','length',
                            'width', 
                            'callsign',
                            'current_port_country'] 

        pfields = default_fields 
        fields_param = ','.join(pfields) 
         
        pname  = requote_uri(str(port_name))
        pcode  = requote_uri(str(port_code))

        vessel_type_filter = '&ship_type_in|in|Cargo%20Vessels|ship_type_in=7' 
        vessel_status_filter = '&navigational_status_in|in|Moored,Stopped|navigational_status_in=Moored,Stopped' 
        vessel_status_filter = '&time_of_latest_position_between|gte|time_of_latest_position_between=1440,525600' 
        port_filter = f'&current_port_in|begins|{pname}|current_port_in={pcode}' 

        #Moored and no dest port
        url = f'https://www.marinetraffic.com/en/data/?asset_type=vessels&columns={fields_param}{vessel_type_filter}{vessel_status_filter}{port_filter}'

        print(f'URL : {url}')

        driver = wire_driver.Chrome(chrome_options=options)
        driver.get(url) 
        
        try:
            agreeLocate =  '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, agreeLocate)))

            driver.find_element(By.XPATH, agreeLocate).click()
            print("Accecpted Terms. popup")
        except Exception as e:
            print(f"Error/ No Accept popup. {e}")

        try:

            request = driver.wait_for_request(data_url_pat, timeout=15)

            if request:
                data = json.loads(brotli.decompress(request.response.body))
                print(data)            

        except TimeoutError:
            print("Request timed-out.")
        finally:
            driver.quit()
            print( data['data']) 