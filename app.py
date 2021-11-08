from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# create a route index.html
@app.route("/")
def home():

    # Find data from mongodb
    mars_table = mongo.db.mars_table.find_one()
    # Return template with data
    return render_template("index.html", mars=mars_table)


# Create a route for the scraping function
@app.route("/scrape")
def scrape():

    # start the scrape function
    mars_data = scrape_mars.scrape_all()

    # Add the scraped data to Mongodb
    mongo.db.mars_table.update({}, mars_data, upsert=True)

    # return to homepage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)