import logging

def configure_logger():
    logging.basicConfig(filename="slack-middleware.log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    
# Call configure_logger() to set up the logger
configure_logger()