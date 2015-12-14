import pymysql
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='bigdata.crqksqwikdb4.us-east-1.rds.amazonaws.com',
                             user='bigdata',
                             password='password',
                             db='Bigdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
