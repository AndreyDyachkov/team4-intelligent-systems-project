import gc
import re
from threading import Thread
from werkzeug.serving import WSGIRequestHandler
from io import BytesIO
from PIL import Image
from flask import Flask, request, render_template
from knowledgeBase import perform_sparql_query
from cnn import imgProcessing, createCNN
import base64

gc.collect()
app = Flask('')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


@app.route('/')
def home():
  return render_template('index.html')


@app.route("/sparql-query", methods=['GET', 'POST'])
def sparqlQuery():
  defaultQuery = """
    SELECT ?label ?threshold
    WHERE {
        ind:kpi3 rdfs:label ?label .
        ind:kpi3 prop:hasMin ?threshold .
    }"""
  queryResult = ""
  if request.method == 'GET':
    print(f"GET request")
    queryResult = perform_sparql_query(defaultQuery)
  if request.method == 'POST':
    print(f"POST request")
    data = request.get_json()
    print(data)
    sparqlQuery = data['text'] or defaultQuery
    deprecate = re.search("(delete)|(update)", sparqlQuery, re.IGNORECASE)
    print(deprecate)
    if deprecate:
      queryResult = "Query is deprecated!"
    else:
      queryResult = perform_sparql_query(sparqlQuery)

  return {"status": "success", "result": queryResult}


@app.route("/check-image", methods=['GET', 'POST'])
def checkImage():
  data = request.get_json()
  image_bytes = BytesIO(base64.b64decode(data['image']))
  img = Image.open(image_bytes)
  width, height = img.size
  X = imgProcessing(image_bytes)
  result = createCNN(X)

  del data
  del image_bytes
  del img
  del X
  gc.collect()

  return {
      "status": "success",
      "result": {
          "cnn": int(result[0]),
          "width": width,
          "height": height
      }
  }


def run():
  WSGIRequestHandler.protocol_version = "HTTP/1.1"
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  print("Server is starting")
  t = Thread(target=run)
  t.start()
