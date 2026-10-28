import unittest
from unittest.mock import patch, Mock  # to simulate API responses & MongoDB queries
import pymongo_referencing_proj        # main file containing functions for testing


class TestStarWars(unittest.TestCase):

    # test 1: checking starships are retrieved correctly from API

    # temporarily replaces real requests.get() with fake version
    # prevents test from making a real API request
    @patch("pymongo_referencing_proj.requests.get")
    def test_get_starships(self, mock_get):

        response = Mock()      # fake HTTP response object created

        response.json.return_value = {             # what fake API returns when .json() is called
            "results": [{"name": "X-wing"}],       # 1 starship returned
            "next": None                           # no more pages
        }

        mock_get.return_value = response           # mocked GET request returns fake response

        result = pymongo_referencing_proj.get_starships()       # calls get_starships() function from main file

        self.assertEqual(len(result), 1)                 # checks returned list contains just 1 starship
        self.assertEqual(result[0]["name"], "X-wing")    # name check of result

    # test 2: check pilot ids are returned from mongodb
    @patch("pymongo_referencing_proj.characters.find_one")
    @patch("pymongo_referencing_proj.requests.get")
    def test_get_pilot_ids(self, mock_get, mock_find):

        response = Mock()
        response.json.return_value = {
            "name": "Luke Skywalker"
        }

        mock_get.return_value = response

        mock_find.return_value = {
            "_id": "12345",
            "name": "Luke Skywalker"
        }

        result = pymongo_referencing_proj.get_pilot_ids(["test-url"])

        self.assertEqual(result, ["12345"])

    # Test 3: Check if missing pilot raises an error
    @patch("pymongo_referencing_proj.characters.find_one")
    @patch("pymongo_referencing_proj.requests.get")
    def test_missing_pilot(self, mock_get, mock_find):

        response = Mock()
        response.json.return_value = {
            "name": "Unknown Pilot"
        }

        mock_get.return_value = response
        mock_find.return_value = None

        with self.assertRaises(ValueError):
            pymongo_referencing_proj.get_pilot_ids(["test-url"])


if __name__ == "__main__":
    unittest.main()