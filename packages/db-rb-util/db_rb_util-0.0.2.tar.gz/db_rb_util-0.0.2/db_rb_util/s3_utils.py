"""Functionality for reading, writing and moving files from AWS S3 bucket."""
import os
from io import BytesIO

import boto3
import pandas as pd

from db_rb_util.logging_utils import get_logger

logger = get_logger("db_logger")

__pdoc__ = {"_get_last_modified": True}


def _get_s3_bucket(*, region_name: str, bucket_name: str):
    """Get S3 bucket resource with specified region."""
    s3_session = boto3.Session(region_name=region_name)
    s3 = s3_session.resource("s3")
    return s3.Bucket(bucket_name)


def read_from_s3(bucketname: str, region: str, filename: str) -> bytes:
    """
    Read any file from S3 bucket.

    Args:
        bucketname (str): S3 bucket name
        region (str): AWS region
        filename (str): name of the input file

    Returns:
        the input file in bytes
    """
    logger.info("Input file: %s/%s", bucketname, filename)

    s3_obj = boto3.client("s3", region_name=region)
    s3_conn = s3_obj.get_object(Bucket=bucketname, Key=filename)
    return s3_conn["Body"].read()


def write_to_s3(file_buffer: BytesIO, region: str, bucketname: str, foldername: str, filename: str):
    """
    Take a file object and save it to the specified location in an S3 bucket.

    Args:
        file_buffer (BytesIO): file content
        region (str): AWS region
        bucketname (str): AWS S3 bucket name
        foldername (str): AWS S3 folder name
        filename (str): save content to this filename

    Returns: None
    """
    s3_session = boto3.Session(region_name=region)
    s3_resource = s3_session.resource("s3")
    filename = os.path.join(foldername, filename)
    s3_resource.Object(bucketname, filename).put(Body=file_buffer.getvalue())


def get_files_batch(*, ext: str, region: str, bucket_name: str, folder: str) -> list[boto3.resources.factory]:
    """
    Find all files that match the selection criteria in <s3://bucket/folder.

    Args:
        ext (str): files extension, should start with a dot
        region (str): AWS region name
        bucket_name (str): The name of the bucket to retrieve files from
        folder (str): refers to the folder containing the source files

    Returns:
        List of S3 objects containing file info
    """
    if ext[0] != ".":
        ext = "." + ext
    bucket = _get_s3_bucket(region_name=region, bucket_name=bucket_name)
    s3_obj_list = []
    for obj in bucket.objects.filter(Prefix=folder):
        if obj.key.endswith(ext):
            s3_obj = obj
            s3_obj_list.append(s3_obj)
            logger.info(f"File {s3_obj.key} found in bucket {bucket_name} matching folder {folder}")
    if len(s3_obj_list) == 0:
        logger.info(f"no files found in {bucket_name}/{folder}")
    return s3_obj_list


def get_files_request(
    *, ext: str, region: str, bucket_name: str, folder: str, file_prefix: str = "", file_suffix: str
) -> list[boto3.resources.factory]:
    """
    Find all files that match the selection criteria latest file in <s3://bucket/folder.

    Args:
        ext (str): files extension, should start with a dot
        region (str): AWS region name
        bucket_name (str): The name of the bucket to retrieve files from
        folder (str): refers to the folder containing the source files
        file_prefix (str): constant string at beginning of file
        file_suffix (str): constant string at end of filename

    Returns:
        List of S3 objects containing file info
    """
    if ext[0] != ".":
        ext = "." + ext
    bucket = _get_s3_bucket(region_name=region, bucket_name=bucket_name)
    s3_obj_list = []
    for obj in bucket.objects.filter(Prefix=folder):
        key = obj.key.split("/")
        if key[len(key) - 1].startswith(f"{file_prefix}") and obj.key.endswith(f"_{file_suffix}{ext}"):
            s3_obj = obj
            s3_obj_list.append(s3_obj)
            logger.info(f"File {s3_obj.key} found in bucket {bucket_name} matching folder {folder}")
    if len(s3_obj_list) == 0:
        logger.info(f"no files found in {bucket_name}/{folder}")
    return s3_obj_list


def get_files_file(*, region: str, bucket_name: str, filekey: str) -> list[boto3.resources.factory]:
    """
    Find the file uploaded in <s3://bucket/folder.

    Args:
        region (str): AWS region name
        bucket_name (str): The name of the bucket to retrieve files from
        filekey (str): file name to be processed

    Returns:
        List of S3 objects containing file info
    """
    bucket = _get_s3_bucket(region_name=region, bucket_name=bucket_name)
    s3_obj_list = []
    for obj in bucket.objects.filter(Prefix=filekey):
        s3_obj_list.append(obj)
        logger.info(f"File {obj.key} found in bucket {bucket_name}")
    if len(s3_obj_list) == 0:
        logger.info(f"no file found in bucket {bucket_name} with key {filekey}")
    return s3_obj_list


def move_s3_file(bucket: str, region: str, key: str, archive_key: str, do_delete: bool) -> None:
    """
    Move a receipt file object to the archive folder.

    Args:
        bucket (str): S3 bucket name
        region (str): AWS region name
        key (str): key for S3 file object
        archive_key (str): new key for the S3 file object copy
        do_delete (bool): flag to indicate if the original object should be deleted

    Returns:
        None
    """
    s3_session = boto3.Session(region_name=region)
    s3 = s3_session.resource("s3")

    try:
        # Copy object key as object archive_key
        obj_new = s3.Object(bucket, archive_key)
        obj_new.copy({"Bucket": bucket, "Key": key})
        # Delete the former object key
        if do_delete:
            obj_old = s3.Object(bucket, key)
            obj_old.delete()
    except Exception as e:
        logger.error(str(e))
        raise e


def write_pdf_to_s3(*, df: pd.DataFrame, region: str, bucketname: str, foldername: str, filename: str):
    """
    Take pandas data frame and write it to csv file on S3.

    Args:
        df (dataframe): pandas data frame to write to S3
        region (str): AWS region name
        bucketname (str): S3 bucket name
        foldername (str): folder in S3 bucket
        filename (str): original filename, used to create new filename

    Returns:
        No return
    """
    csv_buffer = BytesIO()
    df.to_csv(path_or_buf=csv_buffer, sep=",", decimal=".", quotechar='"', encoding="utf-8", index=False, header=True)
    write_to_s3(file_buffer=csv_buffer, region=region, bucketname=bucketname, foldername=foldername, filename=filename)
    logger.info(f"Writing '{filename}' to folder '{foldername}' in bucket '{bucketname}'")
