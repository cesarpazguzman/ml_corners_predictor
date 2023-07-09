import execute_process
import DataCollection.core.logging as logger
import logging
if __name__ == "__main__":
    logger = logging.getLogger("logs").getChild(__name__)
    logger.info("Start application")
    
    execute_process.execute_process(1)