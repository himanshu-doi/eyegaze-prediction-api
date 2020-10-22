"""
Consumer to perform data transformation for the Integrity Breach
Engine and Add them to a new Kafka Topic
"""
import csv
import json
import os
import glob
import requests

from config import FRAMES_PATH
from config import SAVE_PATH
from config import SERVER_URL
from config import LOGGER

CSV_FIELDNAMES = ["file_path",
                  "video_id",
                  "eye_1",
                  "eye_2",
                  "bbox_area",
                  "phi_head",
                  "theta_head",
                  "skew_x",
                  "skew_y"]


class GazePredictionConsumer:
    """
    Custom Consumer for Integrity Breach Model feature transformation
    """

    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.resume_run = os.path.isfile(SAVE_PATH)

    def message_handler(self, msg):
        # msg = json.loads(msg.value())
        payload = json.dumps(msg)

        response = requests.request(
            "POST", SERVER_URL, headers=self.headers, data=payload
        )

        data = {"file_path": msg["file_path"].split('/')[-1],
                "video_id": msg["file_path"].split('/')[-2]}
        if response.status_code == 200:
            data.update(response.json()["data"])
            return data
        return None

    def run(self):
        """Asynchronously consumes data from kafka topic"""
        try:
            with open(SAVE_PATH, "a") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
                if not self.resume_run:
                    writer.writeheader()
                for img_dir in os.listdir(FRAMES_PATH):
                    for frame_id in os.listdir(os.path.join(FRAMES_PATH, img_dir)):
                        file_path = os.path.join(FRAMES_PATH, img_dir, frame_id)
                        print(file_path)
                        msg = {"user_id": "5", "file_path": file_path, "count": 3}
                        if msg:
                            data = self.message_handler(msg)
                        else:
                            LOGGER.error(
                                "Some error in consumer: %s", msg
                            )
                        if data:
                            writer.writerow(data)
                            f.flush()
        except KeyboardInterrupt:
            self.close()

    @staticmethod
    def close():
        """Cleans up any open consumers"""
        # self.consumer.close()
        # close file handler
        LOGGER.info("consumer is closed!!")


if __name__ == "__main__":
    consumer = GazePredictionConsumer()
    consumer.run()
