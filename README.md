# Star Wars MongoDB Project

## Project Overview

This Python project retrieves Star Wars starship data from the SWAPI API and stores it in a local MongoDB database
and then replaces pilot API URLs with MongoDB ObjectIDs referencing existing characters in the database.

## Technologies Used

- Python
- MongoDB
- PyMongo
- Requests
- unittest
- unittest.mock

## How the Program Works

1. Connects to a local MongoDB database called `starwars`.
2. Retrieves starship data from the SWAPI API using HTTP GET requests.
3. Uses pagination to retrieve all available starships.
4. Retrieves pilot information from their API URLs.
5. Searches the existing `characters` collection for matching pilot names.
6. Replaces pilot URLs with MongoDB ObjectIDs.
7. Checks whether each starship already exists in the database.
8. Inserts new starships into the `starships` collection.

## Error Handling

The program includes basic error handling using `try` and `except`.

- API request errors, including timeouts, are handled using `RequestException`.
- Invalid JSON data is handled using `ValueError`, `KeyError` and `TypeError`.
- A `ValueError` is raised if a pilot cannot be found in the MongoDB characters collection.

API requests use a 15-second timeout to prevent indefinite waiting.

## Unit Testing

Unit tests are written using Python's built-in `unittest` library.

`unittest.mock` is used to simulate API responses and MongoDB queries without accessing the real services.

Three tests are included:

1. `test_get_starships` — Checks that starship data is retrieved correctly.
2. `test_get_pilot_ids` — Checks that the correct pilot ID is returned.
3. `test_missing_pilot` — Checks that a missing pilot raises a `ValueError`.

## Running Unit Tests

Run the tests using:

```bash
python3 -m unittest -v test_starwars.py
```
