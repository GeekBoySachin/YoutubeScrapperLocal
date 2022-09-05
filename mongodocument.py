"""
Module to store mongodb Collection documents data
"""


class MongoDocument:
    def __init__(self, thumbnail_image=None, comment_data=None):
        """
        Definition : __init__(thumbnail_image=None, comment_data=None)
        :param thumbnail_image:filetype
        :param comment_data:list(dict)
        """
        self.__thumbnail_image = thumbnail_image
        self.__comment_data = comment_data

    def set_thumbnail_image(self, thumbnail_image):
        """
        :param thumbnail_image:filetype
        :return:None
        """
        self.__thumbnail_image = thumbnail_image

    def set_comment_data(self, comment_data):
        """
        :param comment_data:list(dict)
        :return:None
        """
        self.__comment_data = comment_data

    def get_thumbnail_image(self):
        """
        :return: filetype
        """
        return self.__thumbnail_image

    def get_comment_data(self):
        """
        :return:list(dict)
        """
        return self.__comment_data

    def get_document(self):
        """
        :return: Dictionary
        """
        return {"thumbnail_image": self.__thumbnail_image, "comment_data": self.__comment_data}
