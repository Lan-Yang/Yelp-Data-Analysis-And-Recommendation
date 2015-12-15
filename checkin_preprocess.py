import csv
import json
import pymysql
import pymysql.cursors
import sys
import traceback

DRY_RUN = False

if not DRY_RUN:
	# Connect to the database
	connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# f1_name = "henderson_BLA.csv"
# state = "NV"
# city = "Henderson"

f1_name = "LV_BLA.csv"
state = "NV"
city = "Las Vegas"

business = {}

with open(f1_name) as f:
	reader = csv.reader(f)
	for row in reader:
		bus_id = row[0]
		lng = row[1]
		lat = row[2]
		business[bus_id] = (lng, lat)

checkin = {}
# init checkin
template_daily = {}
for i in range(25):
	template_daily[str(i)] = 0
for bus_id in business:
	checkin[bus_id] = dict(template_daily)

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
		# print bus_id, lng, lat
		for time in check_in:
			checkin_time = time.split('-')[0]
			checkin[bus_id][checkin_time] += 1
print 'Data prepared'

# insert into table
sql = """INSERT INTO `addressw` (`state`,`city`,`longitude`,`latitude`,`checktime`, `weight`) VALUES (%s,%s,%s,%s,%s,%s)"""
data = []
for bus_id, checkins in checkin.iteritems():
	lng = business[bus_id][0]
	lat = business[bus_id][1]
	data += [(state, city, lng, lat, checkin_time, weight) for checkin_time, weight in checkins.iteritems() if weight > 0]
print len(data)

if not DRY_RUN:
	try:
		with connection.cursor() as cursor:
			cursor.executemany(sql, data)
		connection.commit()
	except:
		traceback.print_exc(file=sys.stdout)
		pass
		# break

