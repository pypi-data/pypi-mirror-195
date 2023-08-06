
import logging
logger = logging.getLogger("sttool")

class App:
    
    def __init__(self, settings):
        self.settings = settings    

    def start(self):
        logger.info("sttool Starting")

    def stop(self):
        logger.info("sttool Stopping")
