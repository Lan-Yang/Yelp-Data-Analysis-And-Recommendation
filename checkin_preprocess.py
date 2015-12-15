import csv
import json
import pymysql
import pymysql.cursors
import sys
import traceback

DRY_RUN = True

if not DRY_RUN:
	# Connect to the database
	connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

f1_name = "LV_BLA.csv"
business = {}

with open(f1_name) as f:
	reader = csv.reader(f)
	for row in reader:
		bus_id = row[0]
		lng = row[1]
		lat = row[2]
		business[bus_id] = (lng, lat)

count = 0
f2_name = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_checkin.json"
with open(f2_name) as f:
	for line in f:
		line = line.rstrip()
		obj = json.loads(line)
		bus_id = obj["business_id"]
		if bus_id not in business: continue
		check_in = obj["checkin_info"]
		lng = business[bus_id][0]
		lat = business[bus_id][1]
		# print bus_id, len(check_in)
		count += len(check_in)
		if not DRY_RUN:
			try:
				with connection.cursor() as cursor:	
					for time in check_in:
						checkin_time = time.split('-')[0]
						sql = "INSERT INTO `address` (`state`,`city`,`longitude`,`latitude`,`checktime`) VALUES ('NV','Las Vegas',%s,%s,%s)"
						cursor.execute(sql, (lng, lat, checkin_time))
				connection.commit()
			except:
				traceback.print_exc(file=sys.stdout)
				pass
				# break
print count



