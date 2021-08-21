from mysql.connector import connect, Error

class MySQLManager:

    __connection = None

    def __init__(self):

        self.__connection = self.__get_connection()
        if self.__connection is None:
            print("Connection database error")

    def __get_connection(self):
        try:
            connection = connect(
                    host="localhost",
                    user="root",
                    password="secret",
                    database="cornersSecond",
            )
            return connection
        except Error as e:
            print(e)
            exit(1)

    def execute_many(self, query, records):
        try:
            cursor = self.__connection.cursor()
            cursor.execute_many(query, records)
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

    def close_connection(self):
        self.__connection.close()

