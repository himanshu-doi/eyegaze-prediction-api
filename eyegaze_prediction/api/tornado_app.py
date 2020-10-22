"""
Tornado app for gunicorn
"""
import tornado                                      # pylint: disable=import-error
from tornado.web import Application                 # pylint: disable=import-error

from config import DEBUG
from config import PORT
from eyegaze_prediction.api.controllers import EyegazePredictor
from eyegaze_prediction.api.controllers import HealthCheck
# from tornado.ioloop import IOLoop
# from tornado.web import RequestHandler
# from config import LOGGER


def get_app():
    """
    get tornado app
    :return:
    """
    urls = [
        ("/extract_eyegaze_ml", EyegazePredictor), ("/health-check", HealthCheck)
    ]
    return Application(urls, debug=DEBUG)


def run():
    """
    Sets up the tornado application and adds configurations
    Returns:
        None
    """
    # asyncio.set_event_loop(asyncio.new_event_loop())

    # asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    application = get_app()
    #application.listen(settings.APP.get("port", 80))
    server = tornado.httpserver.HTTPServer(application)
    server.listen(PORT)
    server.start()
    tornado.ioloop.IOLoop.current().start()
