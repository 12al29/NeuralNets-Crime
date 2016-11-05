import re, time, urllib.request
import numpy as np
import os
from datetime import datetime

#calls and retrieves the data set
urllib.request.urlretrieve("https://moto.data.socrata.com/api/views/fjwd-syvh/rows.csv?accessType=DOWNLOAD","Kingston_Police.csv")

def sort_nicely( l ):
    """ Sort the given list in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )
    return l


f = open("Kingston_Police.csv","r")
i=0
#incident_id=[]
incident_date_time=[]
#incident_address = []
incident_type = []
#address_set = set()
incidenttype_set = set()
incident_lat=[]
incident_long=[]
for lines in f:
    if i == 0:
        labels=lines
    else:
        data = lines.split(',')
 #       incident_id+=[data[0]]
        form = '%m/%d/%Y %I:%M:%S %p'
        date_time = datetime.strptime(data[2],form)
        incident_date_time+=[int(time.mktime(date_time.timetuple()))]
        #address_set.add(data[6].lower())
        incidenttype_set.add(data[3].lower())
        incident_type +=[data[3].lower()]
        #incident_address +=[data[6].lower()]
        incident_lat+=[float(data[12])]
        incident_long +=[float(data[13])]
    i+=1
#incident_address_unique = sort_nicely(list(address_set))
incident_type_unique = sort_nicely(list(incidenttype_set))
for x in incident_type:
    val = incident_type_unique.index(x)
    i= incident_type.index(x)
    if (val==0):
        incident_type[i]=[1,0,0,0,0,0]
    elif (val ==1):
        incident_type[i]=[0,1,0,0,0,0]
    elif (val==2):
        incident_type[i]=[0,1,0,0,0,0]
    elif (val==3):
        incident_type[i]=[0,0,1,0,0,0]
    elif (val==4):
        incident_type[i]=[0,0,0,0,1,0]
    elif (val==5):
        incident_type[i]=[0,0,0,0,1,0]
    else:
        incident_type[i]=[0,0,0,0,0,1]

for x in incident_type_unique:
    print(x)
#for x in incident_address:
#   x = incident_address_unique.index(x)

'''
incident_date_time in s since 1970 january 1
incident_address as an int index of the sorted set of alphanumerical blocks
incident_type as a an int index of the sorted set of incident unique types
incident_lat is latitude stored as string
incident_long is longitude stored as string
'''

with open('Kingston_Police_Formatted.csv','a') as out:
    for x in range(len(incident_type)):
        out.write(str(incident_type[x][0])+","+str(incident_type[x][1])+","+str(incident_type[x][2])+","+str(incident_type[x][3])+","+str(incident_type[x][4])+","+str(incident_type[x][5])+","+str(incident_date_time[x])+","+str(incident_lat[x])+","+str(incident_long[x])+"\n")
