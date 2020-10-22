#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download/Upload data blob from GCS bucket
"""
# import os
from google.cloud import storage     # pylint: disable=import-error
# from config import GOOGLE_APPLICATION_CREDENTIALS

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """
    Downloads a blob from the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print("Blob {} downloaded to {}.".format(source_blob_name, destination_file_name))


# download_blob("reco_similar_profile_data","data_similarity.csv",BASE_DIR+"/data_similarity.csv")
# download_blob("reco_similar_profile_data","reco_data_yocket_similarity.csv",BASE_DIR+"/reco_data_yocket_similarity.csv")


def create_bucket(bucket_name):
    """
    Creates a new bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print("Bucket {} created".format(bucket.name))


# create_bucket("reco_similar_profile_data")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


# upload_blob("reco_similar_profile_data","/home/atul/ML/Reco_similarity_docker/data_similarity.csv","data_similarity.csv")
# upload_blob("reco_similar_profile_data","/home/atul/ML/Reco_similarity_docker/reco_data_yocket_similarity.csv","reco_data_yocket_similarity.csv")
