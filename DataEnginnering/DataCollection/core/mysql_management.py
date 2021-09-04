from mysql.connector import connect, Error
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection as SqlAlchemyConnection
import pandas as pd
from properties import properties


class MySQLManager:

    def __init__(self):
        self.__init_connection()
        if self.__connection is None or self.__connection_pd is None:
            print("Connection database error")

    def __init_connection(self):
        try:
            self.__connection = connect(host=properties.mysql_host, user=properties.mysql_user,
                                        password=properties.mysql_password, database=properties.mysql_database)
            self.__connection_pd: SqlAlchemyConnection = create_engine(properties.pymsqyl_url)
        except Error as e:
            print(e)

    def execute_many(self, query: str, records: list):
        try:
            cursor = self.__connection.cursor()
            cursor.executemany(query, records)
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def execute(self, query: str):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query)
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def check_table_exists(self, table: str) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute("SHOW TABLES LIKE '{0}'".format(table))
        result = cursor.fetchone()

        return True if result else False

    def delete_all_records(self, table: str):
        try:
            cursor = self.__connection.cursor()
            cursor.execute("DELETE FROM {0}".format(table))
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def delete_records_by_condition(self, table: str, condition: str):
        try:
            cursor = self.__connection.cursor()
            cursor.execute("DELETE FROM {0} WHERE {1}".format(table, condition))
            self.__connection.commit()
        except Error as err:
            print("Something went wrong: {}".format(err))
            self.close_connection()

    def select_table(self, table: str, where: str = ""):
        try:
            query = 'SELECT * FROM {0} {1}'.format(table,
                                                   "WHERE {0}".format(where) if where else "")
            return pd.read_sql(query, con=self.__connection_pd)
        except Exception as ex:
            print("Something went wrong: {}".format(ex))
            return None

    def close_connection(self):
        self.__connection.close()


