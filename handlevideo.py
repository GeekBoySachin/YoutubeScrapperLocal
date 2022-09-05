"""
Module to handle video download and their upload in Amazon S3 and provide public link
"""
from pytube import YouTube
import os
import logger_class
import boto3
from botocore.exceptions import ClientError


class VideoHandler:
    def __init__(self, url, resolution="low", download_path=os.getcwd()+"\\videos"):
        """
        Definition: __init__(url, resolution="low", download_path=os.getcwd()+"\\videos")
        :param url:video url :str
        :param resolution: low | high :str
        :param download_path: path for saving video :str
        """
        self.url = url
        self.resolution = resolution
        self.download_path = download_path
        self.file_name = None
        self.saved_path = None
        self.logger = logger_class.ScrapperLogger(os.path.basename(__file__)).get_logger()

    def download_video_from_youtube(self):
        """
        Method to download youtube video
        :return:Status True | False  :Boolean
        """
        try:
            yt_obj = YouTube(self.url)
            self.logger.info("Youtube object created")

            if self.resolution == "high":
                stream = yt_obj.streams.get_highest_resolution()
            else:
                stream = yt_obj.streams.get_lowest_resolution()

            self.file_name = "file."+stream.mime_type.split("/")[-1]
            self.logger.info("Starting video download...")
            self.saved_path = stream.download(output_path=self.download_path, filename=self.file_name, max_retries=2)
            self.logger.info("Video download complete")
        except Exception as e:
            self.logger.error(f"Error while downloading video.URL: {self.url}", exc_info=True)
            return False
        else:
            del yt_obj
            self.logger.info(f"Video downloaded for url : {self.url} and saved at :{self.saved_path}")
            return True

    def upload_video_to_s3bucket(self, bucket, save_file_name_s3):
        """
        :param bucket: name of S3 bucket
        :param save_file_name_s3: filename by which it get saved in s3 bucket
        :return:
        """
        s3_client = boto3.client('s3')
        try:
            save_file_name_s3 = "-".join(save_file_name_s3.split(" "))
            response = s3_client.upload_file(self.saved_path, bucket, save_file_name_s3)
        except ClientError as e:
            self.logger.error(f"Error while uploading files in Amazon S3 bucket", exc_info=True)
            return None
        else:
            os.remove(self.saved_path)
            download_url = f"https://{bucket}.s3.ap-south-1.amazonaws.com/{save_file_name_s3}"
            self.logger.info(f"file uploaded in S3 bucket with name :{save_file_name_s3} and download URL is: "
                             f"{download_url}")
            return download_url





