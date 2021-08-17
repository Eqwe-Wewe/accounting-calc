#!/usr/bin/env python

"""
Objects starting with 'random' should be replaced with custom objects.

"""

from data_manager import DataBaseQuery
from root_config import config


with DataBaseQuery(config) as cursor:
    operation = """
                    CREATE TABLE randomdatabase.calculator
                                 (
                                 id int NOT NULL AUTO_INCREMENT,
                                 operation varchar(100) NOT NULL,
                                 result varchar(100) DEFAULT NULL,
                                 date_of_use datetime DEFAULT NULL,
                                 PRIMARY KEY (id)
                                 )ENGINE=InnoDB;
                """
    try:
        cursor.execute(operation)
    except AttributeError as err:
        print(f'AttributeError: {err}')
