"""
Main run file for application
"""
import logging

from tornado.ioloop import IOLoop           # pylint: disable=import-error
from tornado.web import Application         # pylint: disable=import-error

from config import DEBUG
from config import LOGGER
from config import LOGGING_LEVEL
from config import PORT
from eyegaze_prediction.api.controllers import EyegazePredictor
from eyegaze_prediction.api.controllers import HealthCheck


def configure_logging():
    """
    Setting up logger
    Returns:
        None
    """
    logging.basicConfig(
        filename=None,
        level=LOGGING_LEVEL.upper(),
        format="%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def make_app():
    """
    Initialize tornado app
    :return:
    """
    urls = [("/extract_eyegaze_ml", EyegazePredictor), ("/health-check", HealthCheck)]
    return Application(urls, debug=DEBUG)


if __name__ == "__main__":
    print("Starting APP on port %d" % PORT)
    APP = make_app()
    # configure_logging()
    LOGGER.info("Hello!")

    APP.listen(PORT)
    IOLoop.instance().start()
    LOGGER.info("Bye!")
