from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import logger_class
import selectors_repository
import os
import sqldboperations as sqlop
import mongodboperations as mongoop
import video
import mongodocument
import base64
import handlevideo
from credentials import Credentials


class Scrapper:
    def __init__(self, youtubers_videos_section_link, video_count=50):
        """
        Definition : __init__(self,youtuber_videos_link)
        :param youtuber_videos_link:
        """
        self.selector_store = selectors_repository.Selectors()
        self.logger = logger_class.ScrapperLogger(os.path.basename(__file__)).get_logger()
        self.chrome_driver_download_path = os.getcwd()+"\\drivers"
        self.options = self.get_chrome_options()
        self.driver_path = ChromeDriverManager(path=self.chrome_driver_download_path).install()
        self.driver = None
        self.website_link = youtubers_videos_section_link
        self.video_count = video_count

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("--window-size=1366,768")
        options.add_argument("--headless")
        return options

    def open_youtuber_website_in_browser(self):
        """
        :return: None
        """
        try:
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
            self.driver.get(self.website_link)
        except Exception as e:
            self.logger.error(f"Can not open youtuber website {self.website_link} in browser", exc_info=True)
            self.driver.close()
        else:
            self.logger.info("Youtuber website opened in browser.")

    def get_website_element(self, selector_type, selector):
        """
        :param selector_type: str
        :param selector: str
        :return: web element
        """
        try:
            element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((selector_type, selector)))
        except Exception as e:
            self.logger.error(f"Element not found for selector '{selector}' by selector type '{selector_type}'",
                              exc_info=True)
            return None
        else:
            self.logger.info(f"Element found for selector '{selector}' with selector type '{selector_type}'")
            return element

    def get_many_website_elements(self, selector_type, selector):
        """
        :param selector_type:str
        :param selector:str
        :return: list(web element)
        """
        try:
            elements = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((selector_type,
                                                                                                 selector)))
        except Exception as e:
            self.logger.error(f"Elements not found for selector '{selector}' by selector type '{selector_type}'",
                              exc_info=True)
            return None
        else:
            self.logger.info(f"Elements found for selector '{selector}' with selector type '{selector_type}'")
            return elements

    def get_value_from_element(self, element, value_type):
        """
        :param element: web element
        :param value_type: str
        :return: str
        """
        try:
            result = element.get_property(value_type)
            result = self.filter_textcontent(result)
        except Exception as e:
            self.logger.error(f"No such property '{value_type}' for element '{element}'", exc_info=True)
            return None
        else:
            self.logger.info(f"Found result '{result.strip()}' for property '{value_type}' for element '{element}'")
            return result.strip()

    def scroll_videos_page(self, times):
        """
        :param times: int
        :return: None
        """
        self.logger.info("Scrolling page to load video elements in DOM")
        i = 0
        while i < times:
            length = self.driver.execute_script("return window.scrollY")
            self.driver.execute_script("window.scrollTo(arguments[0],arguments[0]+200);", length)
            time.sleep(1)
            i += 1
        self.logger.info("Scrolling complete")

    def find_youtuber_name(self):
        """
        :return: str | None
        """
        element = self.get_website_element(By.CSS_SELECTOR, self.selector_store.get_youtuber_name_css())
        if element is not None:
            youtube_name = self.get_value_from_element(element, "textContent")
            if youtube_name is not None:
                return youtube_name.strip()

    def find_all_video_links(self):
        """
        :return: list(web element) | None
        """
        self.scroll_videos_page(10)
        video_links_list = self.get_many_website_elements(By.CSS_SELECTOR, self.selector_store.get_youtube_videos_css())
        return video_links_list

    def get_title_of_video_video_section(self, element):
        """
        :param element: web element
        :return: str | None
        """
        title_element = element.find_element_by_css_selector(self.selector_store.get_video_title_videos_section_css())
        if title_element is not None:
            title = self.get_value_from_element(title_element, "textContent")
            if title is not None:
                return title

    def get_title_of_video(self):
        """
        :param element: web element
        :return: str | None
        """
        title_element = self.get_website_element(By.CSS_SELECTOR,self.selector_store.get_video_title_css2())
        if title_element is not None:
            title = self.get_value_from_element(title_element, "textContent")
            if title is not None:
                return title

    def find_link_of_video(self, element):
        """
        :param element: web element
        :return: str | None
        """
        link_element = element.find_element_by_css_selector(self.selector_store.get_video_links_css())
        if link_element is not None:
            video_link = self.get_value_from_element(link_element, "href")
            if video_link is not None:
                return video_link

    def find_thumbnail_link(self, video_link):
        """
        :param video_link: str
        :return: str | None
        """
        try:
            response = requests.get(video_link)
            soup = BeautifulSoup(response.text, "html.parser")
            thumbSoupMeta = soup.find("meta", property="og:image")
            thumbnail_image_link = thumbSoupMeta["content"] if thumbSoupMeta else "NotFound"
        except Exception as e:
            self.logger.error(f"Error occurred while fetching thumbnail link for video {video_link} ", exc_info=True)
        else:
            return thumbnail_image_link

    def get_thumbnail_image(self, thumbnail_image_link, name):
        """
        :param thumbnail_image_link: str
        :param name: str
        :return: str | None
        """
        try:
            saved_path = os.getcwd() + "\\thumbnails\\" + name + ".webp"
            response = requests.get(thumbnail_image_link)
            if response.status_code == 200:
                with open(saved_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            self.logger.error(f"Error occurred while fetching thumbnail image for thumbnail {thumbnail_image_link} "
                              , exc_info=True)

    def close_driver(self):
        """
        :return:None
        """
        try:
            self.driver.close()
            self.driver = None
        except Exception as e:
            self.logger.error(f"Error while closing chrome window", exc_info=True)

    def open_video_link(self, video_link):
        """
        :param video_link: str
        :return: Boolean
        """
        try:
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
            self.driver.get(video_link)
        except Exception as e:
            self.logger.error(f"Error while opening chrome window", exc_info=True)
            return False
        else:
            self.logger.info("Video opened in new chrome window")
            return True

    def get_no_of_likes(self):
        """
        :return: str | None
        """
        likes_element = self.get_website_element(By.CSS_SELECTOR, self.selector_store.get_video_likes_css())
        if likes_element is not None:
            likes = self.get_value_from_element(likes_element, "textContent")
            if likes is not None:
                return likes

    def find_no_of_comments(self):
        """
        :return: str | None
        """
        comment_section_element = self.get_website_element(By.CSS_SELECTOR,
                                                           self.selector_store.get_video_comment_section_css())
        if comment_section_element is not None:
            self.logger.info(f"Comment section loaded :{comment_section_element}")
            no_of_comments_element = self.get_website_element(By.XPATH, self.selector_store.get_video_no_comments_xpath())
            if no_of_comments_element is not None:
                no_of_comments = self.get_value_from_element(no_of_comments_element, "textContent")
                if no_of_comments is not None:
                    self.logger.info(f"Found no of comments {no_of_comments}")
                    return no_of_comments

    def get_loaded_comments(self):
        """
        :return: str
        """
        self.logger.info("Scrolling to load comments")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0,500);")
        self.logger.info("Fetching no of comments")
        no_of_comments = self.find_no_of_comments()
        no_of_comments = int(no_of_comments.strip())
        i = 0
        while i < no_of_comments:
            length = self.driver.execute_script("return window.scrollY")
            self.driver.execute_script("window.scrollTo(arguments[0],arguments[0]+100);", length)
            time.sleep(1)
            i += 1
        time.sleep(3)
        self.logger.info("Scroll completed")
        return no_of_comments

    def filter_textcontent(self,comment):
        """Filetring the scrapped text content """
        filters = list(':/.%#@&*()!-_=+ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890? ')
        comment = comment.split(" ")
        comment = " ".join(comment)
        comment = comment.replace("\n", " ")
        for i in range(0, len(comment)):
            if comment[i] not in filters:
                comment = comment.replace(comment[i], " ")
        return comment


    def get_comment_data(self):
        """
        :return: list(Dict)
        """
        commenters_names = None
        comments = None
        commenters_elements = self.get_many_website_elements(By.CSS_SELECTOR,
                                                             self.selector_store.get_video_commenters_name_css())
        if commenters_elements is not None:
            commenters_names = [self.get_value_from_element(element, "textContent")
                                for element in commenters_elements]
        comments_elements = self.get_many_website_elements(By.CSS_SELECTOR,
                                                           self.selector_store.get_video_comments_css())
        if comments_elements is not None:
            comments = [self.get_value_from_element(element, "textContent") for element in comments_elements]
        comment_data = []
        if commenters_names is not None and comments is not None:
            for name, comment in zip(commenters_names, comments):
                if name is not None and comment is not None:
                    name = name.replace(".", " ")  #mongo db does not allow . in key
                    comment_data.append({name: comment})
            self.logger.info(f"Comment scrapped : {comment_data}")
        return comment_data

    def convert_thumbnail_tobase64(self, thumbnail_url):
        """
        "Method to get image content from url and convert it into base64 format
        :param thumbnail_url: str
        :return: base64 str
        """
        try:
            content = requests.get(thumbnail_url).content
            image_as_base64 = base64.b64encode(content)
            self.logger.info("Thumbnail Image converted in base64 format")
            return image_as_base64
        except Exception as e :
            self.logger.error(f"Error while fetching thumbnail image from URL and converting in base64. "
                              f"URL:{thumbnail_url}", exc_info=True)

    def save_thumbnail_image(self, image_as_base64, name):
        """
        Method to convert base64 string into image and save it
        :param image_as_base64:base 64 str
        :param name: path or name of image (.webp) format
        :return:None
        """
        try:
            with open(name, "wb") as fh:
                fh.write(base64.decodebytes(image_as_base64))
        except Exception as e:
            self.logger.error(f"Error while saving image with name{name}", exc_info=True)
        else:
            self.logger.info(f"Image saved with name{name}")

    def download_upload_video_s3bucket(self, video_url, video_name):
        """
        Method will use video handle module class to download and upload video
        :param video_url:
        :param video_name:
        :return:
        """
        bucket = "scrapper-bucket-101"
        hv_object = handlevideo.VideoHandler(video_url)
        hv_object.download_video_from_youtube()
        extension = hv_object.file_name.split(".")[-1]
        video_name = video_name + "." + extension
        down_status = hv_object.download_video_from_youtube()
        if down_status:
            download_url = hv_object.upload_video_to_s3bucket(bucket, video_name)  #video_name = youtubername_1,2,3,4,5
            if download_url is not None:
                return download_url
            else:
                self.logger.error("Some error occurred.")
                return "NoURL"

    def scrap_video_details(self,link, video_obj, document_obj):
        """
        :param link:link of video
        :param video_obj: object of video class
        :param document_obj: objject of mongodocument class
        :return:None
        """
        self.open_video_link(link)
        video_obj.set_video_section_link(self.website_link)
        video_obj.set_video_link(link)
        time.sleep(3)
        video_title = self.get_title_of_video()
        if video_title is not None:
            video_obj.set_video_title(video_title)
        no_of_likes = self.get_no_of_likes()
        if no_of_likes is not None:
            video_obj.set_no_of_likes(no_of_likes)
        self.logger.info("Scrolling to load comments")
        no_of_comments = self.get_loaded_comments()
        if no_of_comments is not None:
            video_obj.set_no_of_comments(no_of_comments)
        # Comment below two lines to disable video upload and download from Amazon S3 bucket
        video_download_link = self.download_upload_video_s3bucket(link, video_title)
        video_obj.set_video_download_link(video_download_link)
        thumbnail_link = self.find_thumbnail_link(link)
        if thumbnail_link is not None:
            video_obj.set_thumbnail_link(thumbnail_link)
            thumbnail_base64 = self.convert_thumbnail_tobase64(thumbnail_link)
            if thumbnail_base64 is not None:
                document_obj.set_thumbnail_image(thumbnail_base64)
        document_obj.set_comment_data(self.get_comment_data())

    def process_request(self):
        """
        :return: result of scrapping
        """
        cred_obj = Credentials()
        self.open_youtuber_website_in_browser()
        time.sleep(3)
        youtuber_name = self.find_youtuber_name()
        links = self.find_all_video_links()
        links = [self.find_link_of_video(i) for i in links]
        self.logger.info(f"Total video found: {str(len(links))}")
        self.close_driver()
        sql_obj = sqlop.SQLOperations(host=cred_obj.get_sql_host(), user=cred_obj.get_sql_user(),
                                      password=cred_obj.get_sql_password())
        mongo_client = mongoop.MongoOperations(mongo_uri=cred_obj.get_mongo_uri())
        result = []
        records_from_db = sql_obj.fetch_videos_by_section_link(self.website_link)
        i = 1
        for link in links:
            if link in records_from_db:
                record = sql_obj.fetch_record_by_video_link(link)
                if len(record) > 0:
                    result.append(record[0])
                    self.logger.info(f"Found record from Database :{str(record)}")
            else:
                if "?v=" not in link:
                    self.logger.info("Skipping video as its a short")
                    continue
                self.open_video_link(link)
                video_obj = video.Video()
                document_obj = mongodocument.MongoDocument()
                if youtuber_name is not None:
                    video_obj.set_youtuber_name(youtuber_name)
                self.scrap_video_details(link, video_obj, document_obj)
                document = document_obj.get_document()
                mongo_document_id = mongo_client.insert_document_into_collection(document)
                video_obj.set_mongo_document_id(str(mongo_document_id))
                record = video_obj.get_record()
                self.logger.info(f"Scraped record saved in Database :{str(record)}")
                sql_obj.insert_record_into_videos_table(record)
                result.append(record)
                del video_obj
                del document_obj
                self.close_driver()
            if i == self.video_count:
                break
            i = i + 1
        if len(result) > 0:
            return True, result
        else:
            return False, None


if __name__ == "__main__":
    obj = Scrapper("https://www.youtube.com/user/krishnaik06/videos", 2)
    status, result = obj.process_request()
    print(status)
    print(result)












