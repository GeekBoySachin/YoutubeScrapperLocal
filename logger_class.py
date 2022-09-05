import logging
import logging.config
import logging.handlers
import yaml


class ScrapperLogger:
    def __init__(self,name):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f.read(),Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
        self.logger = logging.getLogger(name)

    def get_logger(self):
        return self.logger

if __name__=="__main__":
    obj = ScrapperLogger("logger_class.py")
    logger = obj.get_logger()
    logger.info(" your code is failed and their is critical situation")
