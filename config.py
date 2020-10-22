"""
Contains the constants used throughout application
"""
import logging.config
import os
import sys
from pathlib import Path

import watchtower                           # pylint: disable=import-error
from boto3.session import Session           # pylint: disable=import-error
from dotenv import load_dotenv              # pylint: disable=import-error

ENV_PATH = Path(".") / ".env"
load_dotenv(dotenv_path=ENV_PATH)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DETECT = ['mtcnn']   #['mtcnn', 'cv2', 'dnn']
EYE_GAZE_BATCH_SIZE = 10  # equivalent to 5 testing images

EYE1_FEATS = ['eye1_iris_x',
              'eye1_iris_y',
              'eye1_eyeball_x',
              'eye1_eyeball_y',
              'eye1_theta',
              'eye1_phi',
              'eye1_dx',
              'eye1_dy']

EYE2_FEATS = ['eye2_iris_x',
              'eye2_iris_y',
              'eye2_eyeball_x',
              'eye2_eyeball_y',
              'eye2_theta',
              'eye2_phi',
              'eye2_dx',
              'eye2_dy']

HEAD_FEATS = ["bbox_area",
              "phi_head",
              "theta_head",
              "skew_x",
              "skew_y"]

RF_MODEL_PATH = os.path.join(BASE_DIR, "eyegaze_prediction/dependencies/gaze_ml_rf_model_94roc.pkl")
ML_MODEL = os.getenv("ML_MODEL")     # ['rf_model', 'xgb_model']
ML_THRESH = 0.65

# GPU and API Level configurations
GPU_FRACTION = float(os.getenv("EYEGAZE_GPU_FRACTION"))
PORT = int(os.getenv("PORT"))
DEBUG = os.getenv("DEBUG") == "True"
HOST = os.getenv("HOST")

API_VERSION = os.getenv("API_VERSION")
STAGE = os.getenv("STAGE")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_LOG_GROUP = os.getenv('AWS_LOG_GROUP')     # your log group
AWS_LOG_STREAM = os.getenv('AWS_LOG_STREAM')     # your stream
AWS_LOGGER_NAME = os.getenv('AWS_LOGGER_NAME')

############ Setting multiple loggers on different platforms

LOGGER = None
LOGGER_NAME = ''
PLATFORM_ENV = "CONSOLE"
if PLATFORM_ENV == "CONSOLE":
    LOGGER_NAME = "eyegaze-console-logger"
    LOGGER = logging.getLogger(LOGGER_NAME)
    LOGGER.setLevel(logging.INFO)
    LOG_FILE_HANDLER = logging.StreamHandler(sys.stdout)
    LOGGER.addHandler(LOG_FILE_HANDLER)

# elif PLATFORM_ENV == "GCP":
#     CLIENT = google.cloud.logging.Client()
#     HANDLER = CloudLoggingHandler(CLIENT)
#     LOGGER = logging.getLogger(LOGGER_NAME)
#     google.cloud.logging.handlers.setup_logging(HANDLER)

elif PLATFORM_ENV == "AWS":
    BOTO3_SESSION = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )
    HANDLER = watchtower.CloudWatchLogHandler(
        boto3_session=BOTO3_SESSION, log_group=AWS_LOG_GROUP, stream_name=AWS_LOG_STREAM
    )
    LOGGER = logging.getLogger(AWS_LOGGER_NAME)
    LOGGER.addHandler(HANDLER)

if LOGGING_LEVEL == "warning":
    LOGGER.setLevel(logging.WARNING)
elif LOGGING_LEVEL == "error":
    LOGGER.setLevel(logging.ERROR)
elif LOGGING_LEVEL == "debug":
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

# API Consumer variables
FRAMES_PATH = "/home/himanshu/Downloads/gaze_tagging_isc_images"
OUTPUT_CSV = 'frames_output_iter2.csv'
SAVE_PATH = os.path.join(BASE_DIR, OUTPUT_CSV)
SERVER_URL = "http://0.0.0.0:5602/extract_eyegaze_ml"
