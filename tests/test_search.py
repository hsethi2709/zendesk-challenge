"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-28 11:53:48
@modify date 2021-06-28 11:53:48
@desc Search Test Cases
"""
import pytest

from app.controller.search import ZendeskSearch

invalid_user_inputs = [
    ('_id', 'test-string', {'status': False, 'message': 'Invalid ID! Please enter an integer value'}),
    ('_id', '$71', {'status': False, 'message': 'Invalid ID! Please enter an integer value'}),
    ('active', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('verified', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('shared', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('suspended', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('organization_id', 'test-string', {'status': False, 'message': 'Invalid ID! Please enter an integer value'}),
    ('email', 'coffeyrasmussen@flotonic.com', {'status': True, 'data': [
        {'_id': 1,
            'url': 'http://initech.zendesk.com/api/v2/users/1.json',
            'external_id': '74341f74-9c79-49d5-9611-87ef9b6eb75f',
            'name': 'Francisca Rasmussen',
            'alias': 'Miss Coffey',
            'created_at': '2016-04-15T05:19:46 -10:00',
            'active': True,
            'verified': True,
            'shared': False,
            'locale': 'en-AU',
            'timezone': 'Sri Lanka',
            'last_login_at': '2013-08-04T01:03:27 -10:00',
            'email': 'coffeyrasmussen@flotonic.com',
            'phone': '8335-422-718',
            'signature': "Don't Worry Be Happy!",
            'organization_id': 119,
            'tags': ['Springville', 'Sutton', 'Hartsville/Hartley', 'Diaperville'],
            'suspended': True,
            'role': 'admin',
            'organization_name': 'Multron',
            'ticket_0': 'A Nuisance in Kiribati',
            'ticket_1': 'A Nuisance in Saint Lucia'}]}),
    ('email', 'test-string', {'status': False, 'message': 'Invalid Email! Please enter a valid email - example@sample.com'})
]

invalid_organization_inputs = [
    ('_id', 'test-string', {'status': False, 'message': 'Invalid ID! Please enter an integer value'}),
    ('_id', '$71', {'status': False, 'message': 'Invalid ID! Please enter an integer value'}),
    ('shared_tickets', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('name', 'kof', {'status': True, 'data': [{'_id': 105, 'url': 'http://initech.zendesk.com/api/v2/organizations/105.json', 'external_id': '52f12203-6112-4fb9-aadc-70a6c816d605', 'name': 'Koffee', 'domain_names': ['farmage.com', 'extrawear.com', 'bulljuice.com', 'enaut.com'], 'created_at': '2016-06-06T02:50:27 -10:00', 'details': 'MegaCorp', 'shared_tickets': False, 'tags': ['Jordan', 'Roy', 'Mckinney', 'Frost'], 'users': ['Kari Vinson', 'Lee Dotson'], 'ticket_0': 'A Catastrophe in Hungary', 'ticket_1': 'A Catastrophe in Pakistan', 'ticket_2': 'A Nuisance in Nicaragua', 'ticket_3': 'A Catastrophe in Italy', 'ticket_4': 'A Drama in Wallis and Futuna Islands', 'ticket_5': 'A Nuisance in Yemen', 'ticket_6': 'A Problem in Oman', 'ticket_7': 'A Catastrophe in Iran', 'ticket_8': 'A Nuisance in Tokelau', 'ticket_9': 'A Drama in Saint Vincent and The Grenadines', 'ticket_10': 'A Catastrophe in Jordan'}]})
]


invalid_ticket_inputs = [
    ('_id', 'test-string', {'message': 'Invalid ID! Please enter a valid Ticket ID!', 'status': False}),
    ('_id', '2217c$dc-7371-4401-8738-0a8a8aedc08d', {'message': 'Invalid ID! Please enter a valid Ticket ID!', 'status': False}),
    ('has_incidents', 'true', {'status': False, 'message': 'Invalid input type! Acceptable inputs - True/False'}),
    ('organization_id', 'test-string', {'message': 'Invalid ID! Please enter an integer value', 'status': False}),
    ('submitter_id', 'test-string', {'message': 'Invalid ID! Please enter an integer value', 'status': False}),
    ('assignee_id', 'test-string', {'message': 'Invalid ID! Please enter an integer value', 'status': False}),
]
multiple_value_test = [
    ('tags', 'Jordan', {'status': True, 'data': [{'_id': 105, 'url': 'http://initech.zendesk.com/api/v2/organizations/105.json', 'external_id': '52f12203-6112-4fb9-aadc-70a6c816d605', 'name': 'Koffee', 'domain_names': ['farmage.com', 'extrawear.com', 'bulljuice.com', 'enaut.com'], 'created_at': '2016-06-06T02:50:27 -10:00', 'details': 'MegaCorp', 'shared_tickets': False, 'tags': ['Jordan', 'Roy', 'Mckinney', 'Frost'], 'users': ['Kari Vinson', 'Lee Dotson'], 'ticket_0': 'A Catastrophe in Hungary', 'ticket_1': 'A Catastrophe in Pakistan', 'ticket_2': 'A Nuisance in Nicaragua', 'ticket_3': 'A Catastrophe in Italy', 'ticket_4': 'A Drama in Wallis and Futuna Islands', 'ticket_5': 'A Nuisance in Yemen', 'ticket_6': 'A Problem in Oman', 'ticket_7': 'A Catastrophe in Iran', 'ticket_8': 'A Nuisance in Tokelau', 'ticket_9': 'A Drama in Saint Vincent and The Grenadines', 'ticket_10': 'A Catastrophe in Jordan'}]}),
    ('tags', 'Test', {'status': True, 'data': []}),
    ('domain_names', 'farmage.com', {'status': True, 'data': [{'_id': 105, 'url': 'http://initech.zendesk.com/api/v2/organizations/105.json', 'external_id': '52f12203-6112-4fb9-aadc-70a6c816d605', 'name': 'Koffee', 'domain_names': ['farmage.com', 'extrawear.com', 'bulljuice.com', 'enaut.com'], 'created_at': '2016-06-06T02:50:27 -10:00', 'details': 'MegaCorp', 'shared_tickets': False, 'tags': ['Jordan', 'Roy', 'Mckinney', 'Frost'], 'users': ['Kari Vinson', 'Lee Dotson'], 'ticket_0': 'A Catastrophe in Hungary', 'ticket_1': 'A Catastrophe in Pakistan', 'ticket_2': 'A Nuisance in Nicaragua', 'ticket_3': 'A Catastrophe in Italy', 'ticket_4': 'A Drama in Wallis and Futuna Islands', 'ticket_5': 'A Nuisance in Yemen', 'ticket_6': 'A Problem in Oman', 'ticket_7': 'A Catastrophe in Iran', 'ticket_8': 'A Nuisance in Tokelau', 'ticket_9': 'A Drama in Saint Vincent and The Grenadines', 'ticket_10': 'A Catastrophe in Jordan'}]})
]


class TestUserSearch:
    def test_document_retrieval(self):
        assert ZendeskSearch('_id', 71).userSearch() == {'status': True, 'data': [{'_id': 71, 'url': 'http://initech.zendesk.com/api/v2/users/71.json', 'external_id': 'c972bb41-94aa-4f20-bc93-e63dbfe8d9ca', 'name': 'Prince Hinton', 'alias': 'Miss Dana', 'created_at': '2016-04-18T11:05:43 -10:00', 'active': True, 'verified': False, 'shared': False, 'locale': 'zh-CN', 'timezone': 'Samoa', 'last_login_at': '2013-05-01T01:18:48 -10:00', 'email': 'danahinton@flotonic.com', 'phone': '9064-433-892', 'signature': "Don't Worry Be Happy!", 'organization_id': 121, 'tags': ['Davenport', 'Cherokee', 'Summertown', 'Clinton'], 'suspended': False, 'role': 'agent', 'organization_name': 'Hotcâkes', 'ticket_0': 'A Catastrophe in Micronesia', 'ticket_1': 'A Drama in Wallis and Futuna Islands', 'ticket_2': 'A Drama in Australia'}]}

    @pytest.mark.parametrize('parameter, value, expected', invalid_user_inputs)
    def test_invalid_input_search(self, parameter, value, expected):
        print(ZendeskSearch(parameter, value).userSearch())
        assert ZendeskSearch(parameter, value).userSearch() == expected

    def test_any_tag_retrieval(self):
        assert ZendeskSearch('tags', 'Springville').userSearch() == {'status': True, 'data': [{'_id': 1, 'url': 'http://initech.zendesk.com/api/v2/users/1.json', 'external_id': '74341f74-9c79-49d5-9611-87ef9b6eb75f', 'name': 'Francisca Rasmussen', 'alias': 'Miss Coffey', 'created_at': '2016-04-15T05:19:46 -10:00', 'active': True, 'verified': True, 'shared': False, 'locale': 'en-AU', 'timezone': 'Sri Lanka', 'last_login_at': '2013-08-04T01:03:27 -10:00', 'email': 'coffeyrasmussen@flotonic.com', 'phone': '8335-422-718', 'signature': "Don't Worry Be Happy!", 'organization_id': 119, 'tags': ['Springville', 'Sutton', 'Hartsville/Hartley', 'Diaperville'], 'suspended': True, 'role': 'admin', 'organization_name': 'Multron', 'ticket_0': 'A Nuisance in Kiribati', 'ticket_1': 'A Nuisance in Saint Lucia'}]}

    def test_not_found(self):
        assert ZendeskSearch('_id', '3333').userSearch() == {'status': True, 'data': []}


class TestOrganizationSearch:

    def test_document_retrieval(self):
        assert ZendeskSearch('_id', 102).organizationSearch() == {'status': True, 'data': [{'_id': 102, 'url': 'http://initech.zendesk.com/api/v2/organizations/102.json', 'external_id': '7cd6b8d4-2999-4ff2-8cfd-44d05b449226', 'name': 'Nutralab', 'domain_names': ['trollery.com', 'datagen.com', 'bluegrain.com', 'dadabase.com'], 'created_at': '2016-04-07T08:21:44 -10:00', 'details': 'Non profit', 'shared_tickets': False, 'tags': ['Cherry', 'Collier', 'Fuentes', 'Trevino'], 'users': ['Roman Meyers', 'Jaime Dickerson', 'Velasquez Cameron'], 'ticket_0': 'A Problem in Syria', 'ticket_1': 'A Problem in Gambia', 'ticket_2': 'A Problem in Antigua and Barbuda', 'ticket_3': 'A Catastrophe in Bermuda', 'ticket_4': 'A Nuisance in Eritrea', 'ticket_5': 'A Problem in Japan', 'ticket_6': 'A Drama in Martinique', 'ticket_7': 'A Nuisance in Liberia'}]}

    @pytest.mark.parametrize('parameter, value, expected',
                             invalid_organization_inputs)
    def test_invalid_input_search(self, parameter, value, expected):
        assert ZendeskSearch(parameter, value).organizationSearch() == expected

    @pytest.mark.parametrize('parameter, value, expected', multiple_value_test)
    def test_any_tag_retrieval(self, parameter, value, expected):
        assert ZendeskSearch(parameter, value).organizationSearch() == expected


class TestTicketSearch:

    def test_document_retrieval(self):
        assert ZendeskSearch('_id', "2217c7dc-7371-4401-8738-0a8a8aedc08d").ticketSearch() == {'status': True, 'data': [{'_id': '2217c7dc-7371-4401-8738-0a8a8aedc08d', 'url': 'http://initech.zendesk.com/api/v2/tickets/2217c7dc-7371-4401-8738-0a8a8aedc08d.json', 'external_id': '3db2c1e6-559d-4015-b7a4-6248464a6bf0', 'created_at': '2016-07-16T12:05:12 -10:00', 'type': 'problem', 'subject': 'A Catastrophe in Hungary', 'description': 'Ipsum fugiat voluptate reprehenderit cupidatat aliqua dolore consequat. Consequat ullamco minim laboris veniam ea id laborum et eiusmod excepteur sint laborum dolore qui.', 'priority': 'normal', 'status': 'closed', 'submitter_id': 9, 'assignee_id': 65, 'organization_id': 105, 'tags': ['Massachusetts', 'New York', 'Minnesota', 'New Jersey'], 'has_incidents': True, 'due_at': '2016-08-06T04:16:06 -10:00', 'via': 'web', 'user_name': 'Josefa Mcfadden', 'organization_name': 'Koffee'}]}

    @pytest.mark.parametrize('parameter, value, expected',
                             invalid_ticket_inputs)
    def test_invalid_input_search(self, parameter, value, expected):
        assert ZendeskSearch(parameter, value).ticketSearch() == expected

    def test_any_tag_retrieval(self):
        assert len(ZendeskSearch('tags', 'Northern Mariana Islands')
                   .ticketSearch()['data']) == 14
