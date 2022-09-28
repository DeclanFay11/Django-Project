from math import ceil
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# pip install wheel, then https://towardsdatascience.com/install-shapely-on-windows-72b6581bb46c pip install 'C:\Users\Declan Fay\Downloads\Shapely-1.6.4.post2-cp37-cp37m-win_amd64.whl'
from shapely.geometry import Point, Polygon
from datetime import date
from .models import Vessels_in_Port

def marinetraffic_vessels_in_port():

#    Vessels_in_Port.objects.all().delete()
#    return
    options = Options()
    options.add_argument('headless')
    web = webdriver.Chrome(options=options)
    web.get('https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&current_port_in|begins|NEW%20YORK|current_port_in=137&current_port_in|begins|NEW%20YORK|current_port_in=137&time_of_latest_position_between|gte|time_of_latest_position_between=1440,525600&ship_type_in|in|Cargo%20Vessels|ship_type_in=7')


    try:
        agreeLocate = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
        web.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        print("passed accept")
    except TimeoutError:
        print("Error/ no accept on screen")
    finally:
        print("Pass")

    try:
        gettingLocation = WebDriverWait(web, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/span')))
        records = web.find_element(By.XPATH, '//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/span').text
        #print(records)
        numbers = re.findall('[0-9]+', records)
        #print(numbers[0])
        numRecords = int(numbers[0])
        #print(str(numRecords))
        vCoordinates = dict()
        for j in range(0,ceil(numRecords/20)):
            vessels = web.find_elements(By.XPATH, '//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[2]/div/div/a')
            for index in range(0,len(vessels)):
                row = vessels[index].text
                #print(vessels[index].text)
                i = index + 1
                imo = web.find_element(By.XPATH, '//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div['+str(i)+']/div[8]/div/div/div').text
                mmsi = web.find_element(By.XPATH, '//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div['+str(i)+']/div[9]/div/div/div').text
                lat = web.find_element(By.XPATH, '//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div['+str(i)+']/div[13]/div/div/div').text
                lon = web.find_element(By.XPATH, '//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div['+str(i)+']/div[14]/div/div/div').text
                row += " (" + imo + ") " + lat + " " + lon
                vCoordinates.update({vessels[index].text.strip():[lat,lon,imo,mmsi]})
                #print(row)
            #print("Vessel Location")
            if(j < ceil(numRecords/20) - 1):
                web.find_element(By.XPATH, '//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/div/div/div[3]/button[2]').click()

    except TimeoutError:
        print("Error/ no accept on screen")
    finally:
        web.quit()


    # x(lon) and y(lat) coordinates are swapped because of webpage
    PNTCcoords =  [(-74.137609,40.6751336),(-74.1243267,40.6931992),(-74.1539383,40.7026348),(-74.1611266,40.6889528)]
    MAHERcoords = [(-74.1367722,40.6741124),(-74.159872,40.6883401),(-74.1646028,40.6832741),(-74.1412568,40.6676228)]
    GCT_BAYONNEcoords =  [(-74.0980196,40.6750075),(-74.0674639,40.6626707),(-74.0627432,40.6693439),(-74.0935135,40.6793688)]
    GCTNYcoords = [(-74.1964245,40.6448289),(-74.1962528,40.6351245),(-74.180975,40.6345383),(-74.1811466,40.6454801)]
    APMcoords = [(-74.1417611,40.667928),(-74.1571569,40.6733475),(-74.1618347,40.6622801),(-74.1468143,40.6577549)]
    RedHookcoords = [(-74.019227,40.6891317),(-74.0203428,40.6772207),(-74.000473,40.6757235),(-74.0000868,40.6884484)]
    RedHookBROOKcoords = [(-73.9800239, 40.7090113),(-73.9794874, 40.7003737),(-73.9658403, 40.7004225),(-73.9675355, 40.7095968)]
    Manhattancoords = [(-74.0124035, 40.7492727),( -74.0136266, 40.7387381),(-74.0077257, 40.7382992),(-74.0065026, 40.7488826)]

    PNCTpoly = Polygon(PNTCcoords)
    MAHERpoly = Polygon(MAHERcoords)
    GCT_BAYONNEpoly = Polygon(GCT_BAYONNEcoords)
    GCTNYpoly = Polygon(GCTNYcoords)
    APMpoly = Polygon(APMcoords)
    RedHookpoly = Polygon(RedHookcoords)
    RedHookBROOKpoly = Polygon(RedHookBROOKcoords)
    Manhattanpoly = Polygon(Manhattancoords)

    today = date.today()

    # mm/dd/YY
    d1 = today.strftime("%m/%d/%y")
    inPort = ""
    for key, value in vCoordinates.items():
        location = ""
        lat = value[0]
        lon = value[1]
        imo = value[2]
        mmsi = value[3]
        terminal = ""
        location += key + " (IMO:" + imo + ")" + " (MMSI:" + mmsi + ") (lon:" + lon + ",lat:" + lat + ")"

        #inPort += "\"" + d1 + "\"," + key + ",\"" + imo + "\"" + ",\"" + mmsi + "\""
        inPort += "\"" + d1 + "\",\"" + key + "\""

        point = Point(float(lon),float(lat))

        if(PNCTpoly.contains(point)):
            #location += " is located at PNCT"
            inPort += ",PNCT"
            terminal = "PNCT"
        if(MAHERpoly.contains(point)):
            #location += " is located at MAHER"
            inPort += ",MAHER"
            terminal = "MAHER"
        if(GCT_BAYONNEpoly.contains(point)):
            #location += " is located at GCT Bayonne"
            inPort += ",GCT Bayonne"
            terminal = "GCT Bayonne"
        if(GCTNYpoly.contains(point)):
            #location += " is located at GCT NY"
            inPort += ",GCT NY"
            terminal = "GCT NY"
        if(APMpoly.contains(point)):
            #location += " is located at APM"
            inPort += ",APM"
            terminal = "APM"
        if(RedHookpoly.contains(point)):
            #location += " is located at RedHook"
            inPort += ",RedHook"
            terminal = "RedHook"
        if(RedHookBROOKpoly.contains(point)):
            #location += " is located at RedHook BROOKLYN"
            inPort += ",RedHook BROOKLYN"
            terminal = "RedHook BROOKLYN"
        if(Manhattanpoly.contains(point)):
            inPort += ",MANHATTAN"
            terminal = "MANHATTAN"


        inPort += "\n"
        #location += "\n"
        #print(location)
        row = Vessels_in_Port(run_date = today,vessel_name = key,terminal = terminal)
        row.save()
    print(inPort)
    

#    with open("VesselsInNYNJPorts.csv", "w",encoding='utf-8') as f:
#        #f.write("Date,Vessel Name,IMO,MMSI,Terminal\n")
#        f.write("Date,Vessel Name,Terminal\n")
#        f.write(inPort)
#        f.close()