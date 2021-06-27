"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-26 19:13:17
@modify date 2021-06-26 19:13:17
@desc This file contains access to database and performs search as per criteria
"""

import json
import logging
import re
import sys
from typing import Dict, List

from tinydb import Query, TinyDB


class ZendeskDatabase:
    def __init__(self) -> None:
        """Creates a connection to the database
        """
        logging.info("Setting up TinyDB and initiating connection to tables")
        self.db = TinyDB("app/data/zendesk.json")
        self.user_table = self.db.table('users')
        self.organization_table = self.db.table('organizations')
        self.ticket_table = self.db.table('tickets')
        self.query = Query()
        self.searchTerms = {}

    def initializeDatabase(self) -> None:
        """This will read all the json files and create a single database using
        TinyDB for searching. Within the Zendesk database, we will have three
        tables - Users, Organization & Tickets.
        """
        print("Please wait while the little elves draw your map")
        logging.info("Loading data files into database")
        try:
            with open("app/data/organizations.json", "r") as f:
                logging.info("Loading Organization data into db")
                json_data = json.load(f)  # parse its JSON
                searchTerms = []
                # iterate over each entry in the `organizations.json`
                for entry in json_data:
                    searchTerms.extend(list(entry.keys()))
                    self.organization_table.insert(entry)
                self.searchTerms['organizations'] = list(set(searchTerms))

            with open("app/data/users.json", "r") as f:
                logging.info("Loading Users data into db")
                json_data = json.load(f)  # parse its JSON
                searchTerms = []
                # iterate over each entry in the `users.json`
                for entry in json_data:
                    searchTerms.extend(list(entry.keys()))
                    self.user_table.insert(entry)  # insert it in the DB
                self.searchTerms['users'] = list(set(searchTerms))

            with open("app/data/tickets.json", "r") as f:
                logging.info("Loading Tickets data into db")
                json_data = json.load(f)  # parse its JSON
                searchTerms = []
                # iterate over each entry in the `tickets.json`
                for entry in json_data:
                    searchTerms.extend(list(entry.keys()))
                    self.ticket_table.insert(entry)  # insert it in the DB
                self.searchTerms['tickets'] = list(set(searchTerms))
            return True
        except FileNotFoundError as e:
            logging.exception("Data file not found "+e)
            print("One of the data files is missing")
            sys.exit()

    def userSearch(self, parameter, value) -> List[Dict]:
        """User Search in databased based on parameter and value

        Args:
            parameter (str): Criteria for search
            value: Value for search
        """
        logging.info("Searching User with term & value {0} {1}"
                     .format(parameter, value))
        if parameter == 'tags':
            users = self.user_table.search(self.query[parameter].any(value))
        else:
            # Exact match for ID's and Empty values
            if (isinstance(value, int) or
               (isinstance(value, str) and len(value) == 0)):
                users = self.user_table.search(self.query[parameter] == value)
            else:
                # Near match
                users = self.user_table.search(
                    self.query[parameter].matches(value, flags=re.IGNORECASE)
                )
        return users

    def organizationSearch(self, parameter, value) -> List[Dict]:
        """Organization Search in databased based on parameter and value

        Args:
            parameter (str): Criteria for search
            value: Value for search
        """
        logging.info("Searching Organization with term & value {0} {1}"
                     .format(parameter, value))
        if parameter == 'tags' or parameter == 'domain_names':
            organization = self.organization_table.search(
                             self.query[parameter].any(value))
        else:
            # Exact match for ID's and empty values
            if (isinstance(value, int) or
               (isinstance(value, str) and len(value) == 0)):
                organization = self.organization_table.search(
                             self.query[parameter] == value)
            else:
                # Near match
                organization = self.organization_table.search(
                    self.query[parameter].matches(value, flags=re.IGNORECASE)
                )
        return organization

    def ticketSearch(self, parameter, value) -> List[Dict]:
        """Ticket Search in databased based on parameter and value

        Args:
            parameter (str): Criteria for search
            value: Value for search
        """
        logging.info("Searching Tickets with term & value {0} {1}"
                     .format(parameter, value))
        if parameter == 'tags':
            tickets = self.ticket_table.search(
                             self.query[parameter].any(value))
        else:
            # Exact match
            if (isinstance(value, int) or
               (isinstance(value, str) and len(value) == 0)):
                tickets = self.ticket_table.search(
                             self.query[parameter] == value)
            else:
                # Near Match
                tickets = self.ticket_table.search(
                    self.query[parameter].matches(value, flags=re.IGNORECASE)
                    )
        return tickets
