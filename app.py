from flask import Flask, render_template
import urllib.request as request
import pandas as pd
import folium

app = Flask(__name__)

# 讀取車位資料
df_park = pd.read_csv('parking.csv')

# 新增地圖
map = folium.Map([23.5, 121], zoom_start=7, tiles='OpenStreetMap')

from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(map)

for index, row in df_park.iterrows(): 
        information = str(row['ROADNAME']) + '' + str(row['PAYCASH'])
        folium.Marker(location = [row['lat'], row['lon']], popup = information).add_to(marker_cluster)

#map.save('park.html')


# 經緯度轉換(TWD97 -> WGS84)
import geopandas as gpd
# gdf_dig=gpd.read_file('digging.csv')
# gdf_dig.crs = {'init': 'epsg:3826'}
# gdf_dig=gdf_dig.to_crs( 'epsg:4326')
# gdf_dig.to_csv('digging.csv')

# 讀取道路挖掘資料
df_dig = pd.read_csv('digging.csv')
map = folium.Map([23.5, 121], zoom_start=7, tiles='OpenStreetMap')

from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(map)

for index, row in df_dig.iterrows(): 
        information = str(row['CaseStart']) + '~' + str(row['CaseEnd']) + '' + str(row['DigSite'])
        folium.Marker(location = [row['LAT'], row['LONG']], popup = information).add_to(marker_cluster)

#map.save('dig.html')

#使用Geocoding API 將地址轉換為經緯度(因為免費使用有次數限制，所以就先註解了)
import requests
import json
import numpy
StoreData = pd.read_csv('gas station.csv') 
geo=[]
storeaddress = StoreData['address'] 
num=len(StoreData)
if num <5:
        for i in range(storeaddress.size-1):  
                r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + storeaddress[i] + '&key=AIzaSyDSDe5BXTPUec8dAfa44MkqsqslA4Sp484',verify=False)  
                if r.status_code ==200:
                        data=json.loads(r.text) 
                        geo.append(str(data['results'][0]['geometry']['location']['lat']) + ';' + str(data['results'][0]['geometry']['location']['lng']))
  
        df = pd.DataFrame(geo, columns= ['Latitude,Longitude']) 
        df.to_csv(r'gas station.csv', index = False, header=True)
        
else:
        # 讀取加油站資料
        df_gas = pd.read_csv('gas station.csv')
        map = folium.Map([23.5, 121], zoom_start=7, tiles='OpenStreetMap')

        from folium.plugins import MarkerCluster

        marker_cluster = MarkerCluster().add_to(map)

        for index, row in df_gas.iterrows():
                information = str(row['station']) + '' + str(row['address'])
                folium.Marker(location = [row['Latitude'], row['Longitude']], popup = information).add_to(marker_cluster)
        #map.save('gas.html')


# 讀取電動機車資料
df_electric_m = pd.read_csv('electric motorcycle.csv')

map = folium.Map([23.5, 121], zoom_start=7, tiles='OpenStreetMap')

from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(map)

for index, row in df_electric_m.iterrows(): 
        information = str(row["add"]) + '' + "收費方式:"+str(row['fee'])
        folium.Marker(location = [row['Latitude'], row['Longitude']], popup = information).add_to(marker_cluster)

#map.save('electric_m.html')

# 讀取電動汽車資料
df_electric_v = pd.read_csv('electric vehicle.csv')

map = folium.Map([23.5, 121], zoom_start=7, tiles='OpenStreetMap')

from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(map)

for index, row in df_electric_v.iterrows(): 
        information = str(row["add"]) + '' + "收費方式:"+str(row['cha'])
        folium.Marker(location = [row['Latitude'], row['Longitude']], popup = information).add_to(marker_cluster)

#map.save('electric_v.html')

@app.route('/')
def park():
     return render_template('park.html')

@app.route('/dig')
def dig():
     return render_template('dig.html')

@app.route('/gas')
def gas():
    return render_template('gas.html')

@app.route('/electirc_motorcycle')
def electric_m():
     return render_template('electric_m.html')

@app.route('/electirc_vechicle')
def electric_v():
     return render_template('electric_v.html')

if __name__ == '__main__':
    app.run()  

