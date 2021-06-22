#!/usr/bin/env python

"""
Objects starting with 'random' should be replaced with custom objects.

"""

from data_manager import DataBaseQuery
from root_config import config


with DataBaseQuery(config) as cursor:
    operation = """CREATE DATABASE IF NOT EXISTS randomdatabase DEFAULT
                CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"""
    try:
        cursor.execute(operation)
    except AttributeError as err:
        print(f'AttributeError: {err}')
