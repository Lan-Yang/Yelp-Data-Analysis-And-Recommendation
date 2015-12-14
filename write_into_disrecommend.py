import pymysql
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
fname = "disctrict_recommendation_result.csv"
with open(fname) as f:
	for line in f:
		print line
		data = line.split(',')
		if len(data) != 7:
			continue
		state = data[0].strip()
		city = data[1].strip()
		rec1 = data[2].strip()
		rec2 = data[3].strip()
		rec3 = data[4].strip()
		rec4 = data[5].strip()
		rec5 = data[6].strip()
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO `disrecommend` (`state`, `city`, `rec1`, `rec2`, `rec3`, `rec4`, `rec5`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (state, city, rec1, rec2, rec3, rec4, rec5))
			connection.commit()
		except:
			pass
connection.close()