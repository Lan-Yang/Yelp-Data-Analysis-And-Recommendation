import pymysql
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
fname = "user_recommendation_result.csv"
with open(fname) as f:
	for line in f:
		data = line.split(',')
		if len(data) != 6:
			continue
		user_id = data[0][1:-1]
		rec1 = data[1][1:-1]
		rec2 = data[2][1:-1]
		rec3 = data[3][1:-1]
		rec4 = data[4][1:-1]
		rec5 = data[5][1:-3]
		# print user_id, rec5
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO `userrecommend` (`user_id`, `rec1`, `rec2`, `rec3`, `rec4`, `rec5`) VALUES (%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (user_id, rec1, rec2, rec3, rec4, rec5))
			connection.commit()
		except:
			pass
connection.close()