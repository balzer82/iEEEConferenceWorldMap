# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# iEEE Conference World Map

# <codecell>

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import simplekml

# <headingcell level=2>

# Convert Addressto LatLon

# <codecell>

def address2coord(address):
    
    result = None
    while result is None or len(address)>2:
        try:
            url = 'http://maps.googleapis.com/maps/api/geocode/xml'
            payload = {'address': unicode(address), 'sensor': 'true'}
            
            try:
                response = requests.get(url, params=payload)
            except Exception, e:
                print e.message
                return Error(2, "Google", "Google nicht erreichbar.")
        
            if response.status_code != 200:
                print "Can't connect to Google! (status code: " + response.status_code + ")"    
                return Error(response.status_code, "Google", "Google Server nicht erreichbar")
            
            if type(response.content) is unicode:
                soup = BeautifulSoup(response.content.encode('utf8'))
            else:
                soup = BeautifulSoup(response.content)

            #print response.content

            if soup.find('status').string == 'OK':
                #print('Found Location.')
                result = True
                return (soup.find('lat').string , soup.find('lng').string)
            elif soup.find('status').string == 'OVER_QUERY_LIMIT':
                print 'Google API Query Limit reached. Waiting... (maybe you should renew your IP)'
                time.sleep(5)
            elif soup.find('status').string == 'ZERO_RESULTS':
                print '\n' + unicode(address)
                print "not found! Tryin:"
                # Daten oft unsauber, daher immer einen Buchstaben
                # vorn weg lassen
                address=address[1:]
                #print address
            else:
                print '\n' + unicode(address) + '\n'
                print response.url
                print "not found! Giving up..."
                result = True
                return (u'0.0', u'0.0')

        except:
            pass

# <headingcell level=2>

# Crawl the conference search

# <codecell>

# Daten von iEEE Webseite holen
url='http://www.ieee.org/conferences_events/conferences/search/index.html'

# Suchmaske
payload = {'KEYWORDS': '', \
           'CONF_SRCH_RDO': 'conf_date', \
           'RANGE_FROM_DATE': '2014-01-01', \
           'RANGE_TO_DATE': '2014-12-31', \
           'REGION': 'ALL', \
           'COUNTRY': 'ALL', \
           'STATE': 'ALL', \
           'CITY': 'ALL', \
           'SPONSOR': 'ALL', \
           'RowsPerPage': '20000', \
           'PageLinkNum': '1', \
           'ActivePage': '1', \
           'SORTORDER': 'desc', \
           'SORTFIELD': 'start_date'}

# Fire the request
try:
    data = requests.get(url, params=payload)
except Exception, e:
    print e.message
if data.status_code != 200:
    print "Can't connect to iEEE! (status code: " + response.status_code + ")"        

# <headingcell level=2>

# Extract the Data

# <codecell>

# Crawl the Data
soup = BeautifulSoup(data.text)
confs={}
confname=[]
confdate=[]
confloc =[]
conflat =[]
conflon =[]
confurl =[]
for conference in soup.body.find_all('tr', attrs={'class' : ['even','odd']}):
    for idx,infos in enumerate(conference.find_all('td', attrs={'class' : 'pad10'})):
        # Tabelle durchgehen
        # Erste Spalte: Konferenzname
        if idx==0:
            confname.append(infos.a.text.strip())
        # Zweite Spalte: Konferenzdatum
        elif idx==1:
            confdate.append(infos.a.text.strip())
        # Dritte Spalte: Infoseite und Ort
        elif idx==2:
            confurl.append('https://www.ieee.org' + infos.a['href'])
            confloc.append(infos.a.text.strip())

            for br in infos.a.findAll('br'):
                if br.nextSibling == '':
                    pass
                else:
                    adr = br.nextSibling.strip()

            lat,lon = address2coord(adr)
            conflat.append(float(lat))
            conflon.append(float(lon))
        else:
            print(u'Unklar, was das für Daten sind.')
            
confs = zip(confname,confdate,conflat,conflon,confloc,confurl)

# Print the Table           
#for i in range(len(confname)):
#    print('%s findet am %s in %s statt.\n' % (confname[i], confdate[i], confloc[i]))

# <headingcell level=2>

# Clean Data and create KML

# <codecell>

kml = simplekml.Kml()
# Konferenzen löschen, für die kein Ort gefunden wurden
lon=[]
lat=[]

for i in range(len(confs)):
    if confs[i][3] == 0.0:
        pass
    else:
        # KML
        pnt=kml.newpoint(name=confs[i][0], coords=[(confs[i][3],confs[i][2])])
        desct = 'Time: ' + confs[i][1]
        desct += '\nPlace: ' + confs[i][4]
        desct += '\nInfos: ' + confs[i][5]
        pnt.description = desct
        
        # List for Map
        lon.append(confs[i][3])
        lat.append(confs[i][2])

kml.save("iEEE-Conferences.kml")
print('%s von %s Konferenzen ohne Ort.' % (len(confs)-len(lat),len(confs)))
if (len(confs)-len(lat)) == 0:
    print 'Perfect.'
elif (len(confs)-len(lat)) > 5:
    print 'Maybe you should check your Data'

# <headingcell level=2>

# Render the Map

# <headingcell level=3>

# World

# <codecell>

# Thanks to this great tutorial:
# http://peak5390.wordpress.com/2012/12/08/mapping-global-earthquake-activity-a-matplotlib-basemap-tutorial/

map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)
map.drawcoastlines()
map.drawcountries()
#map.fillcontinents(color = 'gray')
map.bluemarble()
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

x,y = map(lon, lat)
map.plot(x, y, 'ro', markersize=6)
plt.title('iEEE Conferences 2014 Worldmap')
plt.savefig('iEEE-Conferences-2014-Worldmap.png', bbox_inches='tight', dpi=300)
plt.show()

# <headingcell level=3>

# Europe

# <codecell>

m = Basemap(llcrnrlon=-14.0,llcrnrlat=32.0,urcrnrlon=44.4,urcrnrlat=55.3,
            resolution='i',projection='stere',lon_0=10.0,lat_0=54.7)

m.drawcoastlines()
m.fillcontinents(color='gray')
# draw parallels and meridians.
#m.drawparallels(np.arange(-40,61.,2.))
#m.drawmeridians(np.arange(0.,43.,2.))
m.drawmapboundary()
m.drawcountries()

x,y = m(lon, lat)
m.plot(x, y, 'ro', markersize=6)


plt.title("European iEEE Conferences 2014")
plt.savefig('iEEE-Conferences-2014-Europe.png', bbox_inches='tight', dpi=300)

plt.show()

# <headingcell level=3>

# USA

# <codecell>

mus = Basemap(llcrnrlon=-125.0,llcrnrlat=20.0,urcrnrlon=-60.0,urcrnrlat=51.4,
            resolution='i',projection='stere',lon_0=-95.0,lat_0=35.0)

mus.drawcoastlines()
mus.fillcontinents(color='gray')
# draw parallels and meridians.
#m.drawparallels(np.arange(-40,61.,2.))
#m.drawmeridians(np.arange(0.,43.,2.))
mus.drawmapboundary()
mus.drawcountries()
mus.drawstates()

x,y = mus(lon, lat)
mus.plot(x, y, 'ro', markersize=6)


plt.title("US iEEE Conferences 2014")
plt.savefig('iEEE-Conferences-2014-USA.png', bbox_inches='tight', dpi=300)

plt.show()

# <codecell>

plt.close()

# <codecell>

print('Done.')

