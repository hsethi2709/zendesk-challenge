"""
@author Harshit Sethi
@email harshit@cognitiveview.com
@create date 2021-06-26 20:05:20
@modify date 2021-06-26 20:05:20
@desc This file extracts statistical information from database
"""

import logging
from typing import Dict, List
from app.model.db import ZendeskDatabase


class ZendeskDatabaseInfo:
    def __init__(self) -> None:
        """Initiates connection to database
        """
        logging.info("Initialising Database helper service")
        self.db = ZendeskDatabase()
        self.db.initializeDatabase()

    def listAllSearchableFields(self) -> Dict[str, List]:
        """Fetches list of all key fields present in documents
        """
        searchableFields = self.db.searchTerms

        return searchableFields
