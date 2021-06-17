import os.path
import csv
import json
from mysql.connector import connect, Error
from config import config


class DataBaseQuery:
    def __init__(self, config):
        self.configuration = config

    def __enter__(self):
        try:
            self.conn = connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Error as err:
            print(err)

    def __exit__(self, exc_type, exc_value, exc_trace):
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except AttributeError as err:
            print(f'AttributeError: {err}')
        if exc_type:
            raise exc_type(exc_value)


class DataManager:
    def __init__(self):
        self.insert_data = []

    @staticmethod
    def write_csv(rows):
        try:
            if not os.path.exists('saves/data.csv'):
                with open('saves/data.csv',
                          'w',
                          newline='',
                          encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([
                        'операции',
                        'результаты',
                        'время'])
            with open('saves/data.csv',
                      'a',
                      newline='',
                      encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(rows)
                print('CSV entry successful!')
        except OSError as err:
            print(f'Exception CSV: {err}')

    @classmethod
    def write_database(self, data):
        with DataBaseQuery(config) as self.cursor:
            self.command = """insert into calculator
                            (operation, result, date_of_use)
                            values
                            (%s, %s, %s);"""
            try:
                self.cursor.executemany(self.command, data)
            except AttributeError as err:
                print(f'AttributeError: {err}')

    @staticmethod
    def write_json(data_to_insert):
        try:
            if not os.path.exists('saves/data.json'):
                with open('saves/data.json', 'w', encoding='utf-8') as file:
                    data = []
                    json_data = json.dumps(data, indent=3)
                    file.write(json_data)

            with open('saves/data.json', 'r') as file:
                json_data = json.load(file)

            with open('saves/data.json', 'w', encoding='utf-8') as file:
                for i in data_to_insert:
                    json_data.append({'operation': i[0],
                                      'result': i[1],
                                      'datetime': i[2]})
                json_data = json.dumps(json_data, indent=3, ensure_ascii=False)
                file.write(json_data)
                print('json entry successful!')
        except OSError as err:
            print(f'Exception JSON: {err}')

    @classmethod
    def write_data(self, data):
        if not os.path.exists('saves'):
            os.mkdir('saves')
        DataManager.write_json(data)
        DataManager.write_csv(data)
        DataManager.write_database(data)
