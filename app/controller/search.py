"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-26 17:45:15
@modify date 2021-06-26 17:45:15
@desc Search Implementation
"""


import ast
import logging
import re
from typing import Dict, List

from app.model.db import ZendeskDatabase


class ZendeskSearch:
    def __init__(self, term, value) -> None:
        """Initialises the search term and search value

        Args:
            term ([str]): Search Term/Criteria
            value : Search Value
        """
        self.term = term
        logging.info("Converting input types to their literals")
        # This will check if the search value is integer or boolean otherwise
        # will just set it as a string
        try:
            self.value = ast.literal_eval(value)
        except Exception:
            self.value = value
        self.db = ZendeskDatabase()

    def userSearch(self) -> Dict:
        """Performing search on user and adding relevant fields from other
           databases

        Returns:
            List[Dict]: List of Users
        """
        response = self.searchInputValidator('Users')
        if response['status']:
            users = self.db.userSearch(self.term, self.value)

            for user in users:

                # Getting relevant organization name
                logging.info("Fetching relevant organizations for user {0}"
                             .format(user['_id']))

                if 'organization_id' in user:
                    organizations = self.db.organizationSearch(
                        "_id",
                        user['organization_id']
                    )
                    if len(organizations) == 1:
                        user['organization_name'] = organizations[0]['name']

                # Getting tickets relevant to the users found in search
                logging.info("Fetching relevant tickets for user {0}"
                             .format(user['_id']))

                tickets = self.db.ticketSearch(
                    "submitter_id",
                    user['_id']
                )
                for i, ticket in enumerate(tickets):
                    user['ticket_'+str(i)] = ticket['subject']
            return {"status": True, "data": users}
        else:
            return response

    def organizationSearch(self) -> List[Dict]:
        """Performing search on organization and adding relevant fields from
        other databases

        Returns:
            List[Dict]: List of Organizations
        """
        response = self.searchInputValidator('Organization')
        if response['status']:
            organizations = self.db.organizationSearch(self.term, self.value)
            for organization in organizations:

                # Getting relevant users
                logging.info("Fetching relevant users for organization {0}"
                             .format(organization['_id']))
                users = self.db.userSearch(
                    "organization_id",
                    organization['_id']
                )
                if len(users) > 0:
                    organization['users'] = [user['name'] for user in users]

                # Getting relevant tickets
                logging.info("Fetching relevant tickets for organization {0}"
                             .format(organization['_id']))
                tickets = self.db.ticketSearch(
                    "organization_id",
                    organization['_id']
                )

                if len(tickets) > 0:
                    for i, ticket in enumerate(tickets):
                        organization['ticket_'+str(i)] = ticket['subject']

            return {"status": True, "data": organizations}
        else:
            return response

    def ticketSearch(self) -> List[Dict]:
        """Performing search on tickets and adding relevant fields from other
           databases

        Returns:
            List[Dict]: List of Tickets
        """
        response = self.searchInputValidator('Tickets')
        if response['status']:
            tickets = self.db.ticketSearch(self.term, self.value)

            for ticket in tickets:

                # Getting relevant users
                logging.info("Fetching relevant users for ticket {0}"
                             .format(ticket['_id']))
                if 'submitter_id' in ticket:
                    users = self.db.userSearch(
                        "_id", ticket['submitter_id']
                    )

                # Assuming submitter_id field has one-to-many relation with
                # ticket
                if len(users) == 1:
                    ticket['user_name'] = users[0]['name']

                # Getting relevant organization name
                logging.info("Fetching relevant organizations for ticket {0}"
                             .format(ticket['_id']))

                if 'organization_id' in ticket:
                    organizations = self.db.organizationSearch(
                        '_id',
                        ticket['organization_id']
                    )
                    if len(organizations) == 1:
                        ticket['organization_name'] = organizations[0]['name']

            return {"status": True, "data": tickets}
        else:
            return response

    def searchInputValidator(self, table) -> Dict:
        """Validates the input based on search term type and return appropriate
        error message
        """
        logging.info("Validating ID inputs")
        # Input Validation - '_id'
        if self.term == '_id' and table in ['Users', 'Organization']:
            if not isinstance(self.value, int):
                return {"status": False,
                        "message": "Invalid ID! Please enter an integer value"}
        elif self.term == '_id' and table == 'Tickets':
            regex = '^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$'
            if (isinstance(self.value, int) or
                    not re.search(regex, self.value)):
                return {"status": False,
                        "message": "Invalid ID! Please enter a " +
                                   "valid Ticket ID!"}

        # Input Validation - email
        elif self.term == 'email':
            logging.info("Validating email format")
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if self.value != '':
                if (isinstance(self.value, int) or
                        not re.search(regex, self.value)):
                    return {"status": False,
                            "message": "Invalid Email! Please enter a valid"
                                       " email - example@sample.com"}

        # Input Validation - boolean fields
        elif self.term in ['suspended', 'active', 'verified', 'shared',
                           'shared_tickets', 'has_incidents']:
            logging.info("Validating boolean type")
            if not isinstance(self.value, bool):
                return {"status": False, "message": "Invalid input type!" +
                        " Acceptable inputs - True/False"}

        # Input Validation - Integer fields
        elif self.term in ['organization_id', 'submitter_id', 'assignee_id']:
            if not isinstance(self.value, int):
                logging.info("Validating Integer fields")
                return {"status": False,
                        "message": "Invalid ID! Please enter an integer value"}

        return {"status": True}
