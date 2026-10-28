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
    while url:                                          # loop while url isn't empty/None. breaks when no pages left
        try:
            response = requests.get(url, timeout=15)    # GET request sent to endpoint, returned is stored in response
            response.raise_for_status()                 # check whether HTTP request resulted in error with status codes
            data = response.json()                      # transform response data from json form to dict & saves to new var

            starships.extend(data["results"])           # adds results returned to empty list
            url = data["next"]                          # retrieves URL of the next API page & updates url var

        except requests.exceptions.RequestException as error:
            print("API Request Failed", error)                  # to catch request related errors
            return []                                           # empty list returned to avoid crashing

        except (ValueError, KeyError, TypeError) as error:      # to handle JSON related errors
            print("Invalid JSON data", error)
            return []

    return starships         # if all works returns list of data


# get pilot ids function
def get_pilot_ids(pilot_urls):         # list of pilot urls passed as parameter
    pilot_ids = []                               # empty list to store IDs from mongoDB

    for pilot_url in pilot_urls:                 # loop through pilot urls
        try:
            response = requests.get(pilot_url, timeout=15)
            response.raise_for_status()
            pilot_data = response.json()

            pilot_name = pilot_data["name"]                          # names for pilots are accessed & stored in variable
            character = characters.find_one({"name": pilot_name})    # searches character collection by name and assigns to var

            if character:                                 # check if character found
                pilot_ids.append(character["_id"])        # if true, adds id to pilot_id list
            else:
                raise ValueError("Pilot not found: ", pilot_name)      # if false error raised

        except requests.exceptions.RequestException as error:
            print("API Request Failed ", error)                        # API error handling
            raise

    return pilot_ids                                                   # returns list of pilot ids


#replace pilot links with ids function
def replace_pilots_and_insert():
    starships = get_starships()                   # calls function & stores list of ships in assigned var

    for ship in starships:                        #loop through ships
        pilot_urls = ship["pilots"]               #retrieves the list of pilot URLs from the current ship dictionary

        pilot_ids = get_pilot_ids(pilot_urls)     #uses prewritten function to get id based on stored urls

        ship["pilots"] = pilot_ids                # reassigns urls with ids stored in pilot_ids
        existing_ship = db.starships.find_one({"url": ship["url"]})
        # searches MongoDB for existing starship with same URL

        if not existing_ship:                     # if ship isn't in database, insert
            db.starships.insert_one(ship)
            print(f"Inserted: {ship['name']}")    # confirmation message

if __name__ == "__main__":
    replace_pilots_and_insert()
    # call function only if this file is run directly
    # main stops testing.py from running apis and db changes
