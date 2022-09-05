"""
Module to store data for Video table records
"""


class Video:
    def __init__(self):
        self.__youtuber_name = "Not Found"
        self.__video_section_link = "Not Found"
        self.__video_link = "Not Found"
        self.__video_title = "Not Found"
        self.__no_of_likes = "Not Found"
        self.__no_of_comments = "Not Found"
        self.__thumbnail_link = "Not Found"
        self.__video_download_link = "Not Found"
        self.__mongo_document_id = "Not Found"

    def set_youtuber_name(self, youtuber_name):
        """
        :param youtuber_name: str
        :return: None
        """
        self.__youtuber_name = youtuber_name

    def set_video_link(self, video_link):
        """
        :param video_link: str
        :return: None
        """
        self.__video_link = video_link

    def set_video_section_link(self,video_section_link):
        """
        :param video_section_link: youtuber video section link
        :return:None
        """
        self.__video_section_link = video_section_link

    def set_video_title(self, video_title):
        """
        :param video_title: str
        :return: None
        """
        self.__video_title = video_title

    def set_no_of_likes(self, no_of_likes):
        """
        :param no_of_likes: str
        :return: None
        """
        self.__no_of_likes = no_of_likes

    def set_no_of_comments(self, no_of_comments):
        """
        :param no_of_comments: str
        :return: None
        """
        self.__no_of_comments = no_of_comments

    def set_thumbnail_link(self, thumbnail_link):
        """
        :param thumbnail_link: str
        :return:None
        """
        self.__thumbnail_link = thumbnail_link

    def set_video_download_link(self, video_download_link):
        """
        :param video_download_link: str
        :return: None
        """
        self.__video_download_link = video_download_link

    def set_mongo_document_id(self, mongo_document_id):
        """
        :param mongo_document_id: str
        :return: None
        """
        self.__mongo_document_id = mongo_document_id

    def get_youtuber_name(self):
        """
        :return: str
        """
        return self.__youtuber_name

    def get_video_link(self):
        """
        :return: str
        """
        return self.__video_link

    def get_video_section_link(self):
        """
        :return: str
        """
        return self.__video_section_link

    def get_video_title(self):
        """
        :return: str
        """
        return self.__video_title

    def get_no_of_likes(self):
        """
        :return: str
        """
        return self.__no_of_likes

    def get_no_of_comments(self):
        """
        :return: str
        """
        return self.__no_of_comments

    def get_thumbnail_link(self):
        """
        :return: str
        """
        return self.__thumbnail_link

    def get_video_download_link(self):
        """
        :return: str
        """
        return self.__video_download_link

    def get_mongo_document_id(self):
        """
        :return: str
        """
        return self.__mongo_document_id

    def get_record(self):
        """
        :return: tuple
        """
        return (self.__youtuber_name, self.__video_section_link, self.__video_link, self.__video_title,
                self.__no_of_likes, self.__no_of_comments,self.__thumbnail_link, self.__video_download_link,
                self.__mongo_document_id)


