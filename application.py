from flask import Flask, jsonify, render_template, request
import pymysql
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
address_db = "address"
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('map.html')

@app.route('/address')
def address_point():
	address = request.args.get('a', "Null", type=str)
	checktime = request.args.get('b', "Null", type=str)
	add_list = address.split(',')
	if len(add_list) != 2:
		return ""
	city = add_list[0].strip()
	state = add_list[1].strip()
	data=[]
	try:
		with connection.cursor() as cursor:
			sql = "SELECT `latitude`, `longitude` FROM `address` WHERE `city`=%s AND `state`=%s AND `checktime`=%s"
			cursor.execute(sql, (city, state, checktime))
			for tmp_list in cursor:
				data.append({'latitude': tmp_list['latitude'], 'longitude': tmp_list['longitude']})
	except:
		pass
	f = {'data': data, 'status': 200} 
	return jsonify(**f)

@app.route('/recommend')
def recommend_terms():
	address = request.args.get('a', "Null", type=str)
	userid = request.args.get('b', "Null", type=str)
	add_list = address.split(',')
	udata = []
	ddata = []
	try:
		with connection.cursor() as cursor:
			sql = "SELECT `rec1`, `rec2`, `rec3`, `rec4`, `rec5` FROM `userrecommend` WHERE `user_id`=%s"
			cursor.execute(sql, (userid))
			result = cursor.fetchone()
			udata.append(result["rec1"]);
			udata.append(result["rec2"]);
			udata.append(result["rec3"]);
			udata.append(result["rec4"]);
			udata.append(result["rec5"]);
	except:
		pass
	if len(add_list) == 2:
		city = add_list[0].strip()
		state = add_list[1].strip()
		try:
			with connection.cursor() as cursor:
				sql = "SELECT `rec1`, `rec2`, `rec3`, `rec4`, `rec5` FROM `disrecommend` WHERE `city`=%s AND `state`=%s"
				cursor.execute(sql, (city, state))
				result = cursor.fetchone()
				ddata.append(result["rec1"]);
				ddata.append(result["rec2"]);
				ddata.append(result["rec3"]);
				ddata.append(result["rec4"]);
				ddata.append(result["rec5"]);
		except:
			pass
	f = {'udata': udata, 'ddata': ddata, 'status': 200}
	return jsonify(**f)



if __name__ == '__main__':
    app.run(debug=True)

