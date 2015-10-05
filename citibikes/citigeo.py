import json
import csv
from geopy.distance import vincenty

#generate stationid-tripcount pair from bike data
triparr = {}
print "opening trip data file..."
with open('bikedatamerge.csv', 'rb') as csvfile:
	tripreader = csv.reader(csvfile)
	for row in tripreader:
		#start station
		if str(row[4]) not in triparr:
			if str(row[8]) not in triparr:
				#end station
				triparr[str(row[8])] = 1
			else:
				triparr[str(row[8])] = triparr[str(row[8])] + 1
		else:
			triparr[str(row[4])] = triparr[str(row[4])] + 1



print "number of unique station in trip data:" + str(len(triparr))
for n in triparr:
	print n
print "finished loading trip data"
print "opening station data"
stationarr = []
import urllib, json
with open('station.json') as data_file:
    stationdata = json.load(data_file)
#array of array
#sorry will fix this later im hungry
for row in stationdata['stationBeanList']:
	if row['statusKey'] == 1: #active station
		temp=[]
		temp.append(row['id'])
		temp.append(row['stationName'].replace(u'\xa0', ' '))
		temp.append(row['latitude'])
		temp.append(row['longitude'])
		stationarr.append(temp)
print "finished loading station data"

#done! now moving to next part...
print "opening parks data"
parksarr = []
with open('parks_centroid.txt', 'rb') as csvfile:
	parkreader = csv.reader(csvfile)
	for row in parkreader:
		parksarr.append(row)
print "finished loading parks data"

print "main loop"
#append distance < 0.5 miles from centroid (9999 if none)
for station in stationarr:
	d = 9999
	stationloc=(station[2],station[3]) #generate lat-long pair of station
	for parks in parksarr:
		parksloc=(parks[12],parks[13])
		temp=vincenty(stationloc,parksloc).miles
		if (temp < 0.5) and (temp < d):
			d = temp
	station.append(d) #append distance

	if str(station[0]) in triparr:
		station.append(triparr[str(station[0])])
	else:
		station.append(0)
print "finised main loop"

#test print
#print stationarr
print "generating outfile"
#outfile
with open('distance.csv', 'wb') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["id","stationname","lat","long","distance","freq"])
	for row in stationarr:
		csvwriter.writerow(row)
print "done!"
