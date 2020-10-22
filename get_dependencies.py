"""
Download eyegaze prediction api dependencies
"""
import os
from zipfile import ZipFile
from google.cloud import storage           # pylint: disable=import-error
from config import LOGGER
from config import RF_MODEL_PATH


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
GOOGLE_APPLICATION_CREDENTIALS = BASE_DIR + "/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


BUCKET_NAME = "isc-video-interview-analysis"
STORAGE_CLIENT = storage.Client()
GCS_MODEL_PATH = 'Proctor_dependencies/GazeML/ELG_trained_models/'
ELG_MODEL1_PATH = os.path.join(BASE_DIR, 'eyegaze_prediction/api/dms/dms/models/gaze/GazeML/outputs/ELG_i60x36_f60x36_n32_m2')
ELG_MODEL2_PATH = os.path.join(BASE_DIR, 'eyegaze_prediction/api/dms/dms/models/gaze/GazeML/outputs/ELG_i180x108_f60x36_n64_m3')
DAT_PATH = os.path.join(BASE_DIR, 'eyegaze_prediction/api/dms/dms/models/gaze/3rdparty')
DAT_FILE = 'shape_predictor_5_face_landmarks.dat'
RF_MODEL = 'gaze_ml_rf_model_94roc.pkl'


# Download the file to a destination
def download_to_local(source_path):      # pylint: disable=too-many-branches too-many-statements
    """
    Downloads api dependencies from GCS bucket
    :param source_path: Path to GCS bucket directory containing dependency files
    :return:
    """

    bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)
    iterator = bucket.list_blobs(prefix=source_path)
    # response = iterator._get_next_page_response()
    # print(response)
    for blob in iterator:
        # print("Blob: {}".format(blob.name))
        # pass
        if os.path.split(ELG_MODEL1_PATH)[1] in blob.name:
            if not os.path.exists(os.path.split(ELG_MODEL1_PATH)[0]):
                os.mkdir(os.path.split(ELG_MODEL1_PATH)[0])
            if not os.path.exists(ELG_MODEL1_PATH):
                try:
                    blob.download_to_filename(ELG_MODEL1_PATH + ".zip")
                    # Create a ZipFile Object and load sample.zip in it
                    with ZipFile(ELG_MODEL1_PATH + ".zip", 'r') as zip_obj:
                        # Extract all the contents of zip file in current directory
                        zip_obj.extractall(os.path.split(ELG_MODEL1_PATH)[0])
                    LOGGER.info('Exported %s to %s', blob.name, ELG_MODEL1_PATH)
                except TimeoutError:
                    raise
                except Exception as e:  # pylint: disable=broad-except
                    LOGGER.error("Exception: %s", e)
        elif os.path.split(ELG_MODEL2_PATH)[1] in blob.name:
            if not os.path.exists(os.path.split(ELG_MODEL1_PATH)[0]):
                os.mkdir(os.path.split(ELG_MODEL1_PATH)[0])
            if not os.path.exists(ELG_MODEL2_PATH):
                try:
                    blob.download_to_filename(ELG_MODEL2_PATH + ".zip")
                    # Create a ZipFile Object and load sample.zip in it
                    with ZipFile(ELG_MODEL2_PATH + ".zip", 'r') as zip_obj:
                        # Extract all the contents of zip file in current directory
                        zip_obj.extractall(os.path.split(ELG_MODEL2_PATH)[0])
                    LOGGER.info('Exported %s to %s', blob.name, ELG_MODEL2_PATH)
                except TimeoutError:
                    raise
                except Exception as e:  # pylint: disable=broad-except
                    LOGGER.error("Exception: %s", e)
        elif DAT_FILE in blob.name:
            # Download trained shape detector
            if not os.path.isdir(DAT_PATH):
                os.mkdir(DAT_PATH)
            if not os.path.isfile(os.path.join(DAT_PATH, DAT_FILE)):
                blob.download_to_filename(os.path.join(DAT_PATH, DAT_FILE))
                LOGGER.info('Exported %s to %s', blob.name, DAT_PATH)
        elif RF_MODEL in blob.name:
            if not os.path.isdir(os.path.split(RF_MODEL_PATH)[0]):
                os.mkdir(os.path.split(RF_MODEL_PATH)[0])
            # Download trained ML estimator
            if not os.path.isfile(RF_MODEL_PATH):
                blob.download_to_filename(RF_MODEL_PATH)
                LOGGER.info('Exported %s to %s', blob.name, os.path.split(RF_MODEL_PATH)[0])
        else:
            pass
    LOGGER.info("Downloaded all estimators!")


if __name__ == '__main__':
    download_to_local(GCS_MODEL_PATH)
