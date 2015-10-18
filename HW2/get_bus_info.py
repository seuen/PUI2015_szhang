import sys
import json
import csv
import urllib2

__author__='Siying Zhang'

 
if __name__=='__main__':
	# Retrieve key and bus number from command line
	key = sys.argv[1]
	busLine = sys.argv[2]

	# Request for json file from url given
	url = urllib2.Request('http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' %(key, busLine))
	request = urllib2.urlopen(url)
	busData = json.load(request)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

	with open(sys.argv[3],'wb+') as csvfile:
		writer = csv.writer(csvfile)

		# Take a list of input into the csv file
		writer.writerow(['Latitude', 'Longitude', 'Stop Name', 'Stop Status']) 

		for i in range(0,len(busData)):
			vehicleLoc = busData[i]['MonitoredVehicleJourney']
			lat = vehicleLoc['VehicleLocation']['Latitude']
			lon = vehicleLoc['VehicleLocation']['Longitude']

			for j in range(0,len(vehicleLoc)):
				if not vehicleLoc['OnwardCalls']:
					stopName = 'N/A'
					stopStatus = 'N/A'
				else:
					stopName = vehicleLoc['OnwardCalls']['OnwardCall'][0]['StopPointName']
					stopStatus = vehicleLoc['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']

				row = [lat, lon, stopName,stopStatus]
				writer.writerow(row)




