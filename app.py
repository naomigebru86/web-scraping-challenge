from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scraper

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = pymongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
  
    mars_dict = mongo.db.collection
    mars_data = mars_scraper.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.replace_one({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)