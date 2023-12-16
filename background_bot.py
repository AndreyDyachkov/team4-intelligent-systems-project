#Flask web-server for keep-alive monitoring of the bot
from threading import Thread
from flask import Flask
app = Flask('')  #create a Flask app and define a route to handle requests to the root URL ("/") and returns the string "I'm alive".
@app.route('/')
def home():
  return "I'm alive"
def run():  # set the host to '0.0.0.0' and the port to 80, and runs the Flask app using the `app.run()` method.
  app.run(host='0.0.0.0', port=80)
def keep_alive():   #start a thread running the `run` function. The thread is created with `Thread(target=run)` and then started with `t.start()`.
  print("Server is starting")
  t = Thread(target=run)
  t.start()
