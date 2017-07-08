from ads_config import get_config
import pyathenajdbc
from pyathenajdbc import connect

config = get_config()
ACCESSKEY = config['ACCESSKEY']
SECRETKEY = config['SECRETKEY']

def formatSpecial(results):
  formatted = []
  for result in results:
    (parcelId, latitude, longitude) = result
    formatted_result = {'parcelId': parcelId, 'latitude': latitude, 'longitude': longitude}
    formatted.append(formatted_result)
  return formatted

def get_data_by_lat_long(latitude, longitude):
  conn = pyathenajdbc.connect(
    s3_staging_dir="s3://zillowtest/zillowdb",
    access_key=ACCESSKEY,
    secret_key=SECRETKEY,
    region_name="us-east-2",
    schema="zillowdb"
  )

  try:
    with conn.cursor() as cursor:
      cursor.execute("""
      select * from zillowdb.zillowtest 
      where latitude = %(latitude)f and longitude = %(longitude)f
      limit 10
      """, {'latitude': latitude, 'longitude': longitude})
      results = cursor.fetchall()
      return formatSpecial(results)
  finally:
      conn.close()

def query_athena(query):
  conn = pyathenajdbc.connect(
    s3_staging_dir="s3://zillowtest/zillowdb",
    access_key=ACCESSKEY,
    secret_key=SECRETKEY,
    region_name="us-east-2",
    schema="zillowdb"
  )

  try:
    with conn.cursor() as cursor:
      cursor.execute(query)
      results = cursor.fetchall()
      return formatSpecial(results)
  finally:
      conn.close()


# How to run?
# First run this from the command line: export FLASK_APP=flask-athena.py
# Then from the command line again, run: flask run -h localhost -p 80
# You should see flask started, probably on port 5000
# Hit http://localhost:5000 on your browser

from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/query')
def run_query():
  query = request.args.get('query')
  results = query_athena(query)
  return jsonify(results)

@app.route('/search')
def search_by_lat_long():
  latitude = float(request.args.get('lat'))
  longitude = float(request.args.get('long'))
  results = get_data_by_lat_long(latitude, longitude)
  return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80')

