"""
Module contains the api controllers
"""
import json

from tornado.web import RequestHandler      # pylint: disable=import-error

from config import API_VERSION
from config import LOGGER
from eyegaze_prediction.api.dms.dms.get_eyegaze import predict_eyegaze
from eyegaze_prediction.business_exception import BusinessException      # pylint: disable=unused-import
from eyegaze_prediction.business_exception import custom_except


class HealthCheck(RequestHandler):  # pylint: disable=too-few-public-methods
    """
    A class to handle health check endpoint requests
    """

    def get(self):
        """
        A function to handle GET requests for HealthCheck Endpoint
        Returns:

        """
        result = custom_except("Could not process request", "Error")
        try:
            result = {"status_code": 200, "message": "Server Up"}
            result["api_version"] = API_VERSION
            self.set_status(200, "Server Up")
        except Exception as e:                          # pylint: disable=broad-except
            LOGGER.error(e.__str__())
            result["error"] = e.__str__()
            self.set_status(500, "Server Down")
        self.write(json.dumps(result))


class EyegazePredictor(RequestHandler):       # pylint: disable=too-few-public-methods
    """
    Predictor class to output headgaze direction predictions and out of screen estimate
    """

    def post(self):
        """
        API which processes one image at a time for headgaze prediction.
        :return:
        """
        response = custom_except("Could not fetch off-screen gaze predictions", status_code=500)
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            # LOGGER.info(data)
            user_id = data.get("user_id")
            file_path = data.get("file_path")
            count = data.get("count")

            if type(file_path) in [str, int, float]:
                LOGGER.exception(TypeError)
                response = custom_except("Invalid input format! Input list of file paths", 400)
                self.set_status(400)
            elif file_path is None:
                response = custom_except("File path list missing", 400)
                self.set_status(400)
            elif len(file_path) == 0:
                response = custom_except("File path list empty", 404)
                self.set_status(404)
            else:
                # predict off screen gaze
                pred_batch = predict_eyegaze(file_path)
                LOGGER.info(pred_batch)

                response["data"] = pred_batch
                response["status_code"] = 200
                response["message"] = "Successfully fetched off-screen gaze predictions"
                response["attributes"] = {
                    "user_id": user_id,
                    "file_path": file_path,
                    "count": count,
                }
                response["api_version"] = API_VERSION
        except BusinessException as e:  # pylint: disable=broad-except
            LOGGER.error(e.__str__())
            response['error'] = e.__str__()
            self.set_status(500)
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.error(e.__str__())
            response['error'] = e.__str__()
            self.set_status(500)

        self.write(json.dumps(response))
