from flask import Flask
from flask import request
import json
app = Flask(__name__)

from pyhive import hive
conn = hive.Connection(host="34.67.213.142", port=10000, username="YOU")
cursor = conn.cursor()
#cursor.execute("SELECT * FROM websearch")
#for result in cursor.fetchall():
#  print(result)


@app.route("/test", methods=['GET'])
def test():
  print("hello")
  return "test"

@app.route("/results", methods=['POST'])
def results():
  print("hello")
  data = request.get_json()
  value = data['term']
  str = 'select `clicks` from websearch where term["searchTerm"] = \"' + value + '\"'
  print(str)
  cursor.execute(str)
  res = list(cursor.fetchall())
  print(res[0][0])
  return {"results": json.loads(res[0][0])}
	
    




@app.route("/trends", methods=['POST'])
def trends():
  data = request.get_json()
  print(data)
  data = request.get_json()
  value = data['term']
  str = 'select sum(myval)from(select explode(clicks) as (mykey,myval)from(select clicks from websearch where term["searchTerm"] = \"' + value +  '\") a) b'
  print(str)
  cursor.execute(str)
  res = list(cursor.fetchall())
  print(res[0][0])
  return {"clicks": res[0][0]}




@app.route("/popularity", methods=['POST'])
def popular():
  data = request.get_json()
  print(data)
  data = request.get_json()
  value = data['url']
  str = 'select sum(myval) from (select explode(clicks) as (mykey,myval) from websearch) a where mykey = \"' + value + '\"'
  print(str)
  cursor.execute(str)
  res = list(cursor.fetchall())
  print(res[0][0])
  return {"clicks": res[0][0]}
  

@app.route("/getBestTerms", methods=['POST'])
def getBestTerms():
  data = request.get_json()
  print(data)
  data = request.get_json()
  value = data['website']
  str = 'Select x.term from (Select b.term, b.c, sum(b.click) as s from (select term, clicks[\"' + value + '\"] as c, site, click from websearch lateral view explode(clicks) s as site, click where clicks[\"' + value + '\"] > 0) b Group By b.term, b.c) x where x.c / x.s > 0.05'
  cursor.execute(str)
  res = list(cursor.fetchall())
  print(res)
  fin = []
  for i in res:
    print(json.loads(i[0]))
    fin.append(json.loads(i[0])['searchTerm'])
  
  return {"best_terms": fin}
