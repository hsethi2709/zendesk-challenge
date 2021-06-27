"""
@author Harshit Sethi
@email hsethi2709@gmail.com
@create date 2021-06-26 19:14:20
@modify date 2021-06-26 19:14:20
@desc This file creates the new database index if not already present and
initialises the application
"""

from app.view.zendeskPrompts import ZendeskPrompts
import os
import logging

logging.basicConfig(filename='app.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    logging.info("Starting Application")
    print("Welcome to Zendesk Search")
    print("\n")

    # Starting the input prompt
    ZendeskPrompts()


if __name__ == "__main__":
    if os.path.exists("app/data/zendesk.json"):
        os.remove("app/data/zendesk.json")
    main()
