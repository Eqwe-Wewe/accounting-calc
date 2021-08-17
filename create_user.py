#!/usr/bin/env python

"""
Objects starting with 'random' should be replaced with custom objects.

"""

from data_manager import DataBaseQuery
from root_config import config


with DataBaseQuery(config) as cursor:
    operation = """
                    CREATE USER   'randomusername'@'localhost'
                    IDENTIFIED BY 'randomuserpassword';
                """
    operation2 = """
                    GRANT SELECT,
                    INSERT ON    randomdatabase.calculator
                    TO           'randomusername'@'localhost';
                """
    try:
        cursor.execute(operation)
        cursor.execute(operation2)
    except AttributeError as err:
        print(f'AttributeError: {err}')
