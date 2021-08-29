from mysql.connector import connect, Error
from sqlalchemy import create_engine
import pandas as pd
from core import properties

class MySQLManager:

    __connection = None
    __connection_pd = None

    def __init__(self):

        self.__connection = self.__get_connection()
        self.__connection_pd = create_engine(properties.pymsqyl_url)
        if self.__connection is None or self.__connection_pd is None:
            print("Connection database error")

    def __get_connection(self):
        try:
            connection = connect(
                    host=properties.mysql_host,
                    user=properties.mysql_user,
                    password=properties.mysql_password,
                    database=properties.mysql_database,
            )
            return connection
        except Error as e:
            print(e)
            exit(1)

    def execute_many(self, query, records):
        try:
            cursor = self.__connection.cursor()
            cursor.executemany(query, records)
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def execute(self, query):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query)
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def check_table_exists(self, table):
        cursor = self.__connection.cursor()
        cursor.execute("SHOW TABLES LIKE '{0}'".format(table))
        result = cursor.fetchone()

        return True if result else False

    def delete_all_records(self, table):
        try:
            cursor = self.__connection.cursor()
            cursor.execute("DELETE FROM {0}".format(table))
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def delete_records_by_condition(self, table, condition):
        try:
            cursor = self.__connection.cursor()
            cursor.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def select_table(self, table):
        try:
            return pd.read_sql('SELECT * FROM {0}'.format(table), con=self.__connection_pd)
        except Exception as ex:
            print("Something went wrong: {}".format(ex))
            exit(-1)

    def close_connection(self):
        self.__connection.close()


