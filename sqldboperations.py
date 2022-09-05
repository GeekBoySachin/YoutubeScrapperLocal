"""
Module for basic operations on SQL tables
"""
import mysql.connector as conn
import logger_class
import os


class SQLOperations:
    def __init__(self, host="localhost", user="", password="", database="youtube_data", videos_table="video"):
        """
        Definition:  __init__(host="localhost", user="", password="")
        :param host:str
        :param user:str
        :param password:str
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__videos_table = videos_table
        self.logger = logger_class.ScrapperLogger(os.path.basename(__file__)).get_logger()
        self.create_database()
        self.create_videos_table()

    def set_host(self, host):
        """
        :param host:str
        :return: None
        """
        self.__host = host

    def set_user(self, user):
        """
        :param user:str
        :return: None
        """
        self.__user = user

    def set_password(self, password):
        """
        :param password:str
        :return: None
        """
        self.__password = password

    def get_host(self):
        """
        :return: str
        """
        return self.__host

    def get_user(self):
        """
        :return: str
        """
        return self.__user

    def get_password(self):
        """
        :return: str
        """
        return self.__password

    def get_database(self):
        """
        :return: str
        """
        return self.__database

    def get_videos_table(self):
        """
        :return: str
        """
        return self.__videos_table

    def get_mysql_connection_object(self, database=False):
        """
        :return: mysql.connector.connection.MySQLConnection
        """
        try:
            if database:
                connection = conn.MySQLConnection(host=self.__host,user=self.__user,password=self.__password,
                                                  database=self.__database)
            else:
                connection = conn.MySQLConnection(host=self.__host,user=self.__user,password=self.__password)
        except Exception as e:
            self.logger.error("Error occurred while connecting to MySQL:", exc_info=True)
        else:
            self.logger.info("Connection established with MYSQL")
            return connection

    def close_mysql_connection(self, connection):
        """
        :param connection: mysql.connector.connection.MySQLConnection
        :return: None
        """
        try:
            connection.close()
        except Exception as e:
            self.logger.error("Error occurred while closing connection:", exc_info=True)
            raise Exception("Error occurred while closing connection:" + str(e))
        else:
            self.logger.info("Connection closed.")

    def create_database(self):
        """
        :return: str
        """
        try:
            connection = self.get_mysql_connection_object()
            cursor = connection.cursor()
            cursor.execute(f"create database if not exists {self.__database}")
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while creating database with name: {self.__database}", exc_info=True)
        else:
            self.logger.info(f"Database created with name :{self.__database}")
            return self.__database

    def create_videos_table(self):
        """
        :return: str | None
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            columns = ["youtuber_name varchar(255)","video_section_link varchar(255)","video_link varchar(255)",
                       "video_title varchar(255)"," no_of_likes varchar(255)","no_of_comments varchar(255)",
                       "thumbnail_link varchar(255)","video_download_link varchar(255)",
                       "mongo_document_id varchar(255)"]
            create_table_video = f'{self.__videos_table}({",".join(columns)})'
            self.logger.info(f"Create video table query: {create_table_video}")
            cursor.execute(f"create table if not exists {create_table_video}")
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while creating table with name: {self.__videos_table}", exc_info=True)
        else:
            self.logger.info(f"Table created with name :{self.__videos_table}")
            return self.__videos_table

    def fetch_videos_by_youtuber(self, youtuber_name):
        """

        :param youtuber_name: str
        :return: list
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select * from {self.__videos_table} where = '{youtuber_name}'")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            return result

    def fetch_all_videos_details(self):
        """
        :return: list
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select * from {self.__videos_table};")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            return result

    def check_records_of_youtuber(self, youtuber_name):
        """
        :param youtuber_name: str
        :return: Boolean
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select * from {self.__videos_table} where youtuber_name = '{youtuber_name}'")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            if len(result) > 0:
                return True
            else:
                return False

    def fetch_record_by_video_link(self, video_link):
        """
        :param video_link: str
        :return: record
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select * from {self.__videos_table} where video_link = '{video_link}'")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            return result

    def fetch_record_by_document_id(self, document_id):
        """
        :param video_link: str
        :return: record
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select video_title from {self.__videos_table} where mongo_document_id = '{document_id}'")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            return result

    def insert_record_into_videos_table(self, record):
        """
        :param record: tuple
        :return: None
        """
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            query = f"insert into {self.__videos_table} values{str(record)};"
            self.logger.info(f"Query for insert{query}")
            cursor.execute(query)
            cursor.close()
            connection.commit()
            self.close_mysql_connection(connection)
            self.logger.info(f"Record inserted successfully into {self.__videos_table} table.")
        except Exception as e:
            self.logger.error(f"Error occurred while inserting record in {self.__videos_table} table", exc_info=True)

    def delete_data_base(self):
        """
        :return: None
        """
        try:
            connection = self.get_mysql_connection_object()
            cursor = connection.cursor()
            cursor.execute(f"drop database {self.__database};")
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while dropping database with name: {self.__database}", exc_info=True)
        else:
            self.logger.info(f"Database dropping with name :{self.__database}")

    def delete_youtuber_videos(self, youtuber_name):
        """
        :param youtuber_name:str
        :return:None
        """
        try:
            connection = self.get_mysql_connection_object()
            cursor = connection.cursor()
            cursor.execute(f"delete from {self.__videos_table} where youtuber_name = '{youtuber_name}';")
            connection.commit()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Some error occurred while deleting {youtuber_name} data",exc_info=True)
        else:
            self.logger.info(f"{youtuber_name} data deleted.")

    def fetch_videos_by_section_link(self,video_section_link):
        """
        :param video_section_link: youtubers video section link
        :return: list(tuples)
        """
        result = []
        try:
            connection = self.get_mysql_connection_object(database=True)
            cursor = connection.cursor()
            cursor.execute(f"select video_link from {self.__videos_table} where video_section_link = '{video_section_link}'")
            result = cursor.fetchall()
            cursor.close()
            self.close_mysql_connection(connection)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching record from {self.__videos_table} table", exc_info=True)
            result = [i[0] for i in result]
            return result
        else:
            self.logger.info(f"Records fetched successfully from {self.__videos_table} table.")
            result = [i[0] for i in result]
            return result


if __name__ == "__main__":
    obj = SQLOperations(host="localhost", user="root", password="root")
    record = ('Krish Naik', 'https://www.youtube.com/user/krishnaik06/videos', 'https://www.youtube.com/watch?v=82fPl5l0vXY', 'Hyperparameter Tuning Using Machine Learning Pipelines', '171', 15, 'https://i.ytimg.com/vi/82fPl5l0vXY/maxresdefault.jpg', 'Not Found', ObjectId('6314fae142fecec3b4986d10'))
    print(obj.insert_record_into_videos_table(record))
    # result = obj.fetch_record_by_video_link("https://www.youtube.com/watch?v=HZ9MUzCRlzI")
    # result = [i[0] for i in result]













