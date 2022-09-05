import pymongo
import os
import logger_class
from bson.objectid import ObjectId


class MongoOperations:
    def __init__(self,mongo_uri="mongodb://127.0.0.1:27017", db_name="youtube_data_db",
                 collection_name="youtube_data_collection"):
        """
        Definition: __init__(mongo_uri="mongodb://127.0.0.1:27017", db_name="youtube_data_db",
                            collection_name="youtube_data_collection")
        :param mongo_uri: connection uri str
        :param db_name:database name str
        :param collection_name: collection name str
        """
        self.mongo_uri= mongo_uri
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.logger = logger_class.ScrapperLogger(os.path.basename(__file__)).get_logger()

    def get_db_name(self):
        """
        :return: str
        """
        return self.__db_name

    def get_collection_name(self):
        """
        :return: str
        """
        return self.__collection_name

    def get_mongo_client(self):
        """
        :return: pymongo.MongoClient
        """
        try:
            # client = pymongo.MongoClient(self.__host, self.__port)
            client = pymongo.MongoClient(self.mongo_uri)
        except Exception as e:
            self.logger.error(f"Can not connect to Mongo Database with URI: {self.mongo_uri}",
                              exc_info=True)
        else:
            return client

    def close_client_connection(self, client):
        try:
            client.close()
        except Exception as e:
            self.logger.error(f"Error while closing {client} client connection",exc_info=True)

    def check_db(self, db_name):
        """
        :param db_name: str
        :return: Boolean
        """
        client = self.get_mongo_client()
        databases = client.list_database_names()
        self.close_client_connection(client)
        if db_name in databases:
            return True
        else:
            return False

    def check_collection(self, db_name, collection_name):
        """

        :param db_name: str
        :param collection_name: str
        :return: boolean
        """
        client = self.get_mongo_client()
        db = client[db_name]
        collections = db.list_collections()
        self.close_client_connection(client)
        if collection_name in collections:
            return True
        else:
            return False

    def insert_document_into_collection(self, document):
        """
        :param document: dict
        :return: object
        """
        try:
            client = self.get_mongo_client()
            db = client[self.__db_name]
            collection = db[self.__collection_name]
            document_id = collection.insert_one(document, bypass_document_validation=True)
            document_id = document_id.inserted_id
            self.close_client_connection(client)
        except Exception as e:
            self.logger.error(f"Error while inserting document in collection {self.__collection_name} inside database"
                              f" {self.__db_name}",exc_info=True)
        else:
            self.logger.info(f"Document inserted in collection {self.__collection_name} inside "
                             f"database {self.__db_name}")
            return document_id

    def insert_many_document_into_collection(self, documents):
        """
        :param documents: list(dict)
        :return: list
        """
        try:
            client = self.get_mongo_client()
            db = client[self.__db_name]
            collection = db[self.__collection_name]
            document_id_list = collection.insert_many(documents,  bypass_document_validation=True).inserted_ids
            self.close_client_connection(client)
        except Exception as e:
            self.logger.error(f"Error while inserting document in collection {self.__collection_name} inside database"
                              f" {self.__db_name}",exc_info=True)
            raise Exception(f"Error while inserting document in collection {self.__collection_name} inside "
                            f"database {self.__db_name}")
        else:
            self.logger.info(f"Document inserted in collection {self.__collection_name} inside "
                             f"database {self.__db_name}")
            return str(document_id_list)

    def search_record_from_collection(self, document_id):
        """
        :param document_id: str
        :return: dict
        """
        try:
            client = self.get_mongo_client()
            db = client[self.__db_name]
            collection = db[self.__collection_name]
            search = {"_id": ObjectId(document_id)}
            self.logger.info(str(search))
            result = collection.find_one(search)
            self.close_client_connection(client)
        except Exception as e:
            print(e)
            self.logger.error(f"Some error occurred while searching document with _id:{document_id}",exc_info=True)
        else:
            self.logger.info(f"Search complete. Result: {result}")
            return result

    def delete_record_from_collection(self, document_id):
        """
        :param document_id: str
        :return: dict
        """
        try:
            client = self.get_mongo_client()
            db = client[self.__db_name]
            collection = db[self.__collection_name]
            collection.delete_one({"_id":document_id})
            self.close_client_connection(client)
        except Exception as e:
            self.logger.error(f"Some error occurred while deleting document with _id:{document_id}",exc_info=True)
        else:
            self.logger(f"Document {document_id} deleted.")


    def delete_collection(self,collection_name):
        """

        :param collection_name: str
        :return: None
        """
        try:
            client = self.get_mongo_client()
            db = client[self.__db_name]
            db.drop_collection(collection_name)
            self.close_client_connection(client)
        except Exception as e:
            self.logger.error(f"Some error occurred while deleting collection {collection_name}", exc_info=True)
        else:
            self.logger(f"Collection {collection_name} deleted.")


    def delete_database(self,db_name):
        """
        :param db_name: str
        :return: None
        """
        try:
            client = self.get_mongo_client()
            client.drop_database(db_name)
            self.close_client_connection(client)
        except Exception as e:
            self.logger.error(f"Some error occurred while deleting database {db_name}", exc_info=True)
        else:
            self.logger(f"Database {db_name} deleted.")

if __name__ == "__main__":
    obj = MongoOperations("mongodb://127.0.0.1:27017")
    print(obj.search_record_from_collection("63153b88cbadbdd1420cd57f"))

