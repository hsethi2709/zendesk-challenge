"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-28 11:53:48
@modify date 2021-06-28 11:53:48
@desc Testing Search Terms
"""
import os
import pytest
from app.controller.listFields import ZendeskDatabaseInfo

# Input & Expected Outcome
output = [
    ('organizations',
        ['_id', 'created_at', 'details',
         'domain_names', 'external_id', 'name',
         'shared_tickets', 'tags', 'url']
     ),
    ('users',
        ['_id', 'active', 'alias', 'created_at', 'email', 'external_id',
         'last_login_at', 'locale', 'name', 'organization_id', 'phone', 'role',
         'shared', 'signature', 'suspended', 'tags',
         'timezone', 'url', 'verified']
     ),
    ('tickets', 
        ['_id', 'assignee_id', 'created_at', 'description', 'due_at',
         'external_id', 'has_incidents', 'organization_id', 'priority',
         'status', 'subject', 'submitter_id', 'tags', 'type', 'url', 'via'])
]


# Setting up and retrieving list of terms
@pytest.fixture
def setup():
    if os.path.exists("app/data/zendesk.json"):
        os.remove("app/data/zendesk.json")
    terms = ZendeskDatabaseInfo().listAllSearchableFields()
    return terms


# testing for each term
@pytest.mark.parametrize('parameter, expected', output)
def test_list_fields(setup, parameter, expected):
    print(setup)
    assert setup[parameter] == expected
