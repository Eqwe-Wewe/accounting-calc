# -*- coding: utf-8 -*-

import os.path
import traceback
import csv
import json
import mysql.connector
from contextlib import contextmanager
from config import config


class database_query:
    def __init__(self, config):
        self.configuration = config

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except (mysql.connector.Error) as err:
            print(err)

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type:
            raise exc_type(exc_value)


class DataManager:
    def __init__(self):
        self.insert_data = []  # данные на запись

    @staticmethod
    def write_csv(rows):
        try:
            if not os.path.exists('saves/data.csv'):
                with open('saves/data.csv', 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(['операции', 'результаты', 'время'])
            with open('saves/data.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(rows)
                print('CSV entry successful!')
        except OSError as err:
            print(f'Exception CSV: {err}')
            with open('err_report/report_csv.txt', 'w') as file:
                traceback.print_exc(file=file)

    @classmethod
    def write_database(self, data):
        with database_query(config) as self.cursor:
            self.command = """insert into calculator"""\
                          """(operation, result, date_of_use)"""\
                          """values(%s, %s, %s);"""
            self.cursor.executemany(self.command, data)

    @staticmethod
    def write_json(data_to_insert):
        try:
            if not os.path.exists('saves/data.json'):
                with open('saves/data.json', 'w') as file:
                    data = []
                    json_data = json.dumps(data, indent=3)
                    file.write(json_data)

            with open('saves/data.json', 'r') as file:
                json_data = json.load(file)

            with open('saves/data.json', 'w') as file:
                for i in data_to_insert:
                    json_data.append({'operation': i[0],
                                      'result': i[1],
                                      'datetime': i[2]})
                json_data = json.dumps(json_data, indent=3, ensure_ascii=False)
                file.write(json_data)
                print('json entry successful!')
        except OSError:
            with open('err_report/json_report.txt', 'w') as file:
                traceback.print_exc(file=file)

    @classmethod
    def write_data(self, data):
        if not os.path.exists('saves'):
            os.mkdir('saves')
        if not os.path.exists('err_report'):
            os.mkdir('err_report')
        DataManager.write_json(data)
        DataManager.write_csv(data)
        DataManager.write_database(data)
