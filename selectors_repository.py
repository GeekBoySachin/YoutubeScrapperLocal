"""
Module to store selectors for Youtube website elements

"""


class Selectors:
    def __init__(self):
        self.__youtuber_name_css = "#meta > #channel-name > #container> #text-container>#text"
        self.__youtube_videos_css = "ytd-grid-video-renderer.style-scope.ytd-grid-renderer"
        self.__video_title_css = "a#video-title"
        self.__video_title_css2 = "h1.title.style-scope.ytd-video-primary-info-renderer"
        self.__video_links_css = "a#thumbnail"
        # self.__video_likes_css = ".ytd-watch-metadata > #top-level-buttons-computed > .style-scope:nth-child(1) #text"
        self.__video_likes_css = "yt-formatted-string.style-scope.ytd-toggle-button-renderer.style-text"
        self.__video_no_comments_xpath = '//*[@id="count"]/yt-formatted-string/span[1]'
        self.__video_comment_section_css = "div#main"
        self.__video_commenters_name_css = "a#author-text"
        self.__video_comments_css = "yt-formatted-string#content-text"

    def get_youtuber_name_css(self):
        return self.__youtuber_name_css

    def get_youtube_videos_css(self):
        return self.__youtube_videos_css

    def get_video_title_css(self):
        return self.__video_title_css

    def get_video_links_css(self):
        return self.__video_links_css

    def get_video_likes_css(self):
        return self.__video_likes_css

    def get_video_title_videos_section_css(self):
        return self.__video_title_css

    def get_video_title_css2(self):
        return self.__video_title_css2

    def get_video_no_comments_xpath(self):
        return self.__video_no_comments_xpath

    def get_video_comment_section_css(self):
        return self.__video_comment_section_css

    def get_video_commenters_name_css(self):
        return self.__video_commenters_name_css

    def get_video_comments_css(self):
        return self.__video_comments_css


