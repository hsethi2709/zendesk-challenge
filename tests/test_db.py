"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-28 11:53:48
@modify date 2021-06-28 11:53:48
@desc Testing Database creation
"""
import os
import pytest
from app.model.db import ZendeskDatabase


@pytest.fixture
def setup():
    if os.path.exists("app/data/zendesk.json"):
        os.remove("app/data/zendesk.json")
    db = ZendeskDatabase()
    return db


class TestDatabase:
    def test_database_tables(self, setup):
        assert len(setup.db.tables()) == 3

    def test_database_table_names(self, setup):
        assert setup.db.tables() == {'tickets', 'organizations', 'users'}