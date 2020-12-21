# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 10:14:02 2014

this extracts drifter data based on time range, geographic range and/or drifter id, then plots them.
The ouput html file will be named by 'sink_<region>.html' in same folder as this program. 
input values: time period,gbox(maxlon, minlon,maxlat,minlat),or time period and id
function used: getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid,point_in_poly
output : a plot html file to show drifter track on google map.

Modifications by JiM in March 2019 to:
  - use instead the "gmplot" package instead of Huanxin's "basemap_xu"
  - deliniate by month and length of track
Note that we still need to run a sed command to add key after running this
"""

import datetime as dt
import sys
import os
import pytz
import numpy as np
import gmplot # JiM added this after "pip install gmplot"
from drifter_functions import getobs_drift_byrange,getobs_drift_byid,point_in_poly,hexcolors
ops=os.defpath
pydir='../'
sys.path.append(pydir)

#################Input values#############################################
# HARDCODES ##########
#case='sink_liz_gsc' # name the case study with PI and region
case='sink_cadrin_nshore'
input_time=[dt.datetime(1980,1,1,0,0,0,0,pytz.UTC),dt.datetime(2020,10,15,0,0,0,0,pytz.UTC)] # start time and end time
#gbox=[-70.035594,-70.597883,42.766619,42.093197] #  maxlon, minlon,maxlat,minlat for Stellwagen
#gbox=[-69.33,-69.75,41.5,41.] #  maxlon, minlon,maxlat,minlat for Nant shoals for Cap Brady
#gbox=[-66.,-67.,42.0,41.5] # Liz Brokks NEP
#gbox=[-68.5,-69.3833,41.5, 40.75] # Liz Brooks GSC square case
gbox=[-69.5,-71.,43.,41.5] #north shore
#gbox=[-69.3833, -68.5, -68.5, -68.75,41.5, 41.5, 40.75, 40.75] #where she actually wanted polygon longitude:  
months=[1,2,3,4,5,6,7,8,9,10,11,12] # months of interest
numweeks=6 # number of weeks to track
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#

days=dt.timedelta(days=numweeks*7) # maximum number of day to plot where, for example, 6*7 is six weeks
polygon=[(gbox[0],gbox[2]),(gbox[0],gbox[3]),(gbox[1],gbox[3]),(gbox[1],gbox[2])] #set polygon in case of a square
#polygon=[(gbox[0],gbox[4]),(gbox[1],gbox[5]),(gbox[3],gbox[6]),(gbox[4],gbox[7])  
time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
#mymap = basemap_xu.maps(np.mean(lats), np.mean(lons), 12)  #set center point of the map
id=list(set(ids))
colors=hexcolors(len(id))  #get hex colors,like '00FF00'
gmap3 = gmplot.GoogleMapPlotter(np.mean([gbox[2],gbox[3]]),np.mean([gbox[0],gbox[1]]), 7)
for k in range(len(id)):
      time,ids,lat,lon=getobs_drift_byid(id[k],input_time)  # get data by id
      for z in range(len(lat)-1):  # make plotting drifter start in gbox
         if (time[z]-time[0]<days) and (time[z].month>=months[0]) and (time[z].month<=months[-1]): # ignore tracks beyond "days" long and months outside of "months"
            inside=point_in_poly(lon[z],lat[z],polygon) 
            if inside == True:  
               lat=lat[z:]  # delete data which are before coming in the polygon
               lon=lon[z:]
               time=time[z:]
               title='id:'+str(id[k])+'  time on this point:'+time[0].strftime('%d-%m-%Y %H:%M')
               #mymap.addpoint(lat[0],lon[0], colors[k],title) #plot them
               #mymap.addpath(path,colors[k])
               gmap3.plot(lat,lon,colors[k], edge_width = 2.5) 
               break
ranges=[(gbox[2],gbox[0]),(gbox[3],gbox[0]),(gbox[3],gbox[1]),(gbox[2],gbox[1]),(gbox[2],gbox[0])] #plot range you gave
#gmap3.plot(ranges[0],ranges[1],color[0],edgewidth=10)
#gmap3.plot([gbox[2],gbox[2],gbox[3],gbox[3],gbox[2]],[gbox[0],gbox[1],gbox[1],gbox[0],gbox[0]],colors[0],edgewidth=10)
#gmap3.plot([gbox[4],gbox[5],gbox[6],gbox[7],gbox[4]],[gbox[0],gbox[1],gbox[2],gbox[3],gbox[0]],colors[0],edgewidth=10)

#mymap.addpath(ranges,'red')#00FF00    
#mymap.draw('./sink_through'+dt.datetime.now().strftime('%Y-%m-%d %H:%M')+'.html')
gmap3.draw('/net/pubweb_html/drifter/test.html')


#gmap does not have a apikey function, so lets substitute it.
#os.system(sed '/<\/body>/i <script async defer src="https:\/\/maps.googleapis.com\/maps\/api\/js?v=3&client=gme-noaa&channel=NMFS.NEFSC.OCB.DRIFTERS&callback=initMap"><\/script>' test.html > sink_pi_region.html 
'''
tempHolder=''
oldLine='</body>'
newLine='</script><script async defer src="https://maps.googleapis.com/maps/api/js?v=3&client=gme-noaa&channel=NMFS.NEFSC.OCB.DRIFTERS&callback=initMap"></script></body>'
#Open the file created by gmplot, do a find and replace. 
#My file is in flask, so it is in static/map.html, change path to your file
with open('/net/pubweb_html/drifter/test.html') as fh:
   for line in fh:
       tempHolder += line.replace(oldLine,newLine)
fh.close
#Now open the file again and overwrite with the edited text
fh=open('/net/pubweb_html/drifter/test.html', 'w')
fh.write(tempHolder)
fh.close
'''
