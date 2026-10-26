# Importing libraries
# requests allows python to communicate with APIs via HTTP
import requests
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
# pymongo library for working with mongodb
# client url connects to mongodb server

db = client["starwars"]        # select database to use
characters = db["characters"]  # references for collections
starships = db["starships"]


# Get starships function
def get_starships():
    url = "https://swapi.dev/api/starships/"  # API endpoint stored in variable
    starships = []                            # empty list created to store starship data from API

# could use try and except here for timeout
    while url:                                      # while url isn't empty
        response = requests.get(url, timeout=15)    # GET request sent to endpoint, returned is stored in response
        response.raise_for_status()                 # check whether HTTP request resulted in an error
        data = response.json()                      # transform response data into json form save to new var

        starships.extend(data["results"])
        url = data["next"]

    return starships

get_starships() # call function


# get pilot ids function
def get_pilot_ids(pilot_urls):
    pilot_ids = []

    for pilot_url in pilot_urls:
        response = requests.get(pilot_url, timeout=15)
        response.raise_for_status()
        pilot_data = response.json()

        pilot_name = pilot_data["name"]
        character = db.characters.find_one({"name": pilot_name})

        if character:
            pilot_ids.append(character["_id"])
        else:
            raise ValueError("Pilot not found")

    return pilot_ids


#replace pilot links with ids function
def replace_pilots_and_insert():
    starships = get_starships()

    for ship in starships:
        pilot_urls = ship["pilots"]

        pilot_ids = get_pilot_ids(pilot_urls)

        ship["pilots"] = pilot_ids
        existing_ship = db.starships.find_one({"url": ship["url"]})

        if not existing_ship:
            db.starships.insert_one(ship)
            print(f"Inserted: {ship['name']}")
ships = get_starships()

replace_pilots_and_insert()
