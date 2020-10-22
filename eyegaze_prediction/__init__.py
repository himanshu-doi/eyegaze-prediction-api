"""
    Initialization for the app
"""
import os
import pickle
import tensorflow as tf       # pylint: disable=import-error
from sklearn.ensemble import RandomForestClassifier            # pylint: disable=import-error
from tensorflow.python.client import device_lib                # pylint: disable=import-error
from config import BASE_DIR
from config import GPU_FRACTION
from config import LOGGER
from config import STAGE
from config import ML_MODEL
from config import RF_MODEL_PATH
from eyegaze_prediction.accessories.download_data_bucket import download_blob
from eyegaze_prediction.business_exception import BusinessException


if STAGE == 'dev':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BASE_DIR + "/key.json"
elif STAGE == 'prod':
    pass

# Set logging verbosity to avoid GPU logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.logging.set_verbosity(
    tf.compat.v1.logging.ERROR
)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}

# GPU Configuration
# if "OMP_NUM_THREADS" not in os.environ:
#     os.environ["OMP_NUM_THREADS"] = "8"
# tqdm.write("Tensorflow using {} threads.".format(os.environ["OMP_NUM_THREADS"]))

# Check if GPU is available
SESS_CONFIG = tf.compat.v1.ConfigProto(
    gpu_options=tf.compat.v1.GPUOptions(
        allow_growth=True,
        per_process_gpu_memory_fraction=GPU_FRACTION))
SESS_CONFIG.log_device_placement = False
GPU_AVAILABLE = False
try:
    gpus = [d for d in device_lib.list_local_devices(config=SESS_CONFIG)
            if d.device_type == 'GPU']
    GPU_AVAILABLE = len(gpus) > 0
except:           # pylint: disable=bare-except
    pass
SESS = tf.compat.v1.Session(config=SESS_CONFIG)
SESS_FD = tf.compat.v1.Session(config=SESS_CONFIG)

LOGGER.info("Loading ML Estimator..")
if ML_MODEL == 'rf_model':
    GAZE_MODEL = pickle.load(open(RF_MODEL_PATH, "rb"))
else:
    raise BusinessException("[!] Incorrect ML model specified [!]")

LOGGER.info("Done!")
