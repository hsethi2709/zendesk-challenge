"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-27 11:30:07
@modify date 2021-06-27 11:30:07
@desc This file will display the prompts and call required services
"""

import sys
import time
import logging
from PyInquirer import prompt
from app.controller.search import ZendeskSearch
from app.controller.listFields import ZendeskDatabaseInfo


class ZendeskPrompts:
    def __init__(self) -> None:
        logging.info("Initialising Zendesk Prompts")
        self.searchTerms = ZendeskDatabaseInfo().listAllSearchableFields()
        self.displayPrompts()

    def displayPrompts(self) -> None:
        """Display appropriate prompts for user input and maintains the command
        loop
        """
        try:
            input('Press Enter to continue. Once we are in, you can press ' +
                  'Ctrl+C anytime to exit')
            print("\n")

            while True:
                question = [{
                    'type': 'list',
                    'name': 'search_choice',
                    'message': 'What would you like to do?',
                    'choices': ['1. Search Zendesk', '2. See a list of all '
                                + 'searchable fields', '3. Quit']
                    }]

                answer = prompt(question)

                if answer['search_choice'] == '1. Search Zendesk':
                    self.searchPrompts()
                elif answer['search_choice'] == ('2. See a list of all ' +
                                                 'searchable fields'):
                    self.displayResults(self.searchTerms, 'list')
                    input("Press any key to continue.")
                else:
                    print("Thank you for using Zendesk Search! See you next" + 
                          " time!")
                    sys.exit()
        except Exception:
            print("Thank you for using Zendesk Search! See you next time!")
            sys.exit()
        except KeyboardInterrupt:
            print("\nThank you for using Zendesk Search! See you next time!")
            sys.exit()

    def searchPrompts(self) -> None:
        """Display appropriate search prompts and displays the results
        """

        # Table Choice question
        question = [{
                'type': 'list',
                'name': 'search_table',
                'message': 'Select the option you would like to search',
                'choices': ['Users', 'Organizations', 'Tickets']

            }]
        answer = prompt(question)

        # Getting list of search terms as per table choice
        if answer['search_table'] == 'Users':
            searchTerms = self.searchTerms['users']
        elif answer['search_table'] == 'Organizations':
            searchTerms = self.searchTerms['organizations']
        else:
            searchTerms = self.searchTerms['tickets']

        # Asking user for the field and value they want to search on
        question = [{
            'type': 'list',
            'name': 'search_term',
            'message': "Select the field you would like to search",
            'choices': (searchTerms)
        },
            {
            'type': 'input',
            'name': 'value',
            'message': "Enter the value"
        }]

        # Invalid input loop
        invalidInput = True
        while invalidInput:
            searchAnswer = prompt(question)
            term = searchAnswer['search_term']
            value = searchAnswer['value']

            # Display possible search terms
            if answer['search_table'] == 'Users':
                start_time = time.time()
                results = ZendeskSearch(term, value).userSearch()
            elif answer['search_table'] == 'Organizations':
                start_time = time.time()
                results = ZendeskSearch(term, value).organizationSearch()
            else:
                start_time = time.time()
                results = ZendeskSearch(term, value).ticketSearch()

            # Checking input results
            if results['status']:
                print("Found {0} results in {1} seconds.".format(
                    len(results['data']),
                    time.time() - start_time))
                print()

                # Displaying results
                if len(results['data']) != 0:
                    self.displayResults(results['data'], 'search')
                    print()
                    input("Press any key to continue.")
                else:
                    print("No results found!")
                return
            else:
                print(results['message']+"\n")

    def displayResults(self, results, choice) -> None:
        """Displaying results in suitable format according the user choice
        """
        # Search results
        if choice == 'search':
            for result in results:
                for key, value in result.items():
                    print("{0:18} |  {1}".format(key, value))
                print("-"*50)
        else:
            # List of search terms
            for searchChoice in results:
                print("Search "+searchChoice.title()+" with\n")
                print(*sorted(results[searchChoice]), sep="\n")
                print("-"*50)
