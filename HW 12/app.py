from flask import Flask, render_template
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def index():
    mars = list(db.mars.find())
    return render_template("index.html", mars=mars[0])

@app.route("/scrape")
def mar_info():
    from scrape_mars import scrape
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    db.mars.drop()
    db.mars.insert_one(scrape())
    return render_template("index.html", mars=mars[0])


if __name__ == "__main__":
    app.run(debug=True)