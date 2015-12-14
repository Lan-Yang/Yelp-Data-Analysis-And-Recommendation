from pyspark.sql import SQLContext, Row
from pyspark import SparkContext


sc = SparkContext()
sqlContext = SQLContext(sc)
# sc is an existing SparkContext.

lines = sc.textFile("/Users/nanyazhuo/Documents/bigdata/project/business.csv")
parts = lines.map(lambda l: l.split(","))

people = parts.map(lambda p: Row(id=p[0][1:-1], name=p[1][1:-1], category=p[2][1:-1], state=p[3][1:-1], city=p[4][1:-1], stars=p[5][1:-1]))




# Infer the schema, and register the SchemaRDD as a table.
schemaPeople = sqlContext.inferSchema(people)
schemaPeople.registerTempTable("people")

# SQL can be run over SchemaRDDs that have been registered as a table.
business_id = sqlContext.sql("SELECT name, city, state FROM people WHERE state = 'NV' AND stars = '5.0' ORDER BY city ASC")
#count = sqlContext.sql("SELECT COUNT(*),state as cnt FROM people GROUP BY state ORDER BY cnt DESC")

#./bin/spark-submit --driver-memory=4098m /usr/local/Cellar/spark/1.py

business_id = business_id.map(lambda p:"city: " + p.city + ", state: " + p.state + ", recommendation: " + p.name)

#for count in count.collect():
#	print count
for business_id in business_id.collect():
	print business_id
