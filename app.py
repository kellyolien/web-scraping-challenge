from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars_dict = mongo.db.mars.find_one()
    return render_template("index.html", data="mars_dict")

@app.route("scrape")
def scrape():
    mars_scrape = scrape_mars.scrape()
    print(mars_scrape)

if __name__ ==  "__main__":
    app.run(debug=True)
