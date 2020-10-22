"""
Main run file for application
"""
# import asyncio
import logging

from tornado.web import Application         # pylint: disable=import-error

from config import DEBUG
from config import LOGGER
from config import LOGGING_LEVEL
from config import PORT
from eyegaze_prediction.api import tornado_app
from eyegaze_prediction.api.controllers import EyegazePredictor
from eyegaze_prediction.api.controllers import HealthCheck
# from tornado.ioloop import IOLoop           # pylint: disable=import-error


def configure_logging():
    """
    Setting up logger
    Returns:
        None
    """
    logging.basicConfig(
        filename=None,
        level=LOGGING_LEVEL,
        format="%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_app():
    """
    Initialize tornado app
    :return:
    """
    urls = [("/extract_eyegaze_ml", EyegazePredictor), ("/health-check", HealthCheck)]
    return Application(urls, debug=DEBUG)

APP = get_app()

if __name__ == "__main__":
    # configure_logging()
    LOGGER.info("Starting APP on port %d", PORT)
    LOGGER.info("Hello!")
    tornado_app.run()
    LOGGER.info("Bye!")
