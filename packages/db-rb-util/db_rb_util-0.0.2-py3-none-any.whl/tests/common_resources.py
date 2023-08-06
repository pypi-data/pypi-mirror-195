"""Read test files."""
import io
import json
import os
import xml.etree.ElementTree as ET

import boto3
import pandas as pd

resourcepath = os.path.dirname(os.path.abspath(__file__))
TEST_RESOURCES_DIR = os.path.join(resourcepath, "resources")
AWS_MOTO_REGION = "us-east-1"


def read_test_resource_csv(filename: str, **kwargs) -> pd.DataFrame:
    """
    Read a csv test resource file to a pandas dataframe.

    Supports several pandas.read_csv parameters needed for the tests.

    Args:
        filename: str, file name --> path is fixed
        header: how to set column names in df
        keep_default_na: how to handle standard na values in input
        na_values: possible additional values to read in as NaN
        index_col: use col as index

    Returns: pandas dataframe
    """
    filepath = os.path.join(TEST_RESOURCES_DIR, filename)
    df = pd.read_csv(filepath_or_buffer=filepath, decimal=".", quotechar='"', encoding="utf-8", **kwargs)
    return df


def read_test_resource_json(filename: str) -> dict:
    """
    Read a json test resource file.

    Args:
        filename: str, file name --> path is fixed

    Returns: list
    """
    filepath = os.path.join(TEST_RESOURCES_DIR, filename)
    with open(filepath) as f:
        json_file = json.load(f)
    return json_file


def read_test_resource_sql(filename: str) -> str:
    """
    Read a sql test resource file.

    Args:
        filename: str, file name --> path is fixed

    Returns: list
    """
    filepath = os.path.join(TEST_RESOURCES_DIR, filename)
    return open(filepath, "r").read()


def read_test_resource_pkl(filename: str, **kwargs) -> pd.DataFrame:
    """
    Read a pickle test resource file.

    Args:
        filename: str, file name --> path is fixed

    Returns: dataframe
    """
    filepath = os.path.join(TEST_RESOURCES_DIR, filename)
    return pd.read_pickle(filepath, **kwargs)


def read_test_resource_xml(xml_file: str, **kwargs) -> pd.DataFrame:
    """
    Read a csv test resource file to a pandas dataframe.

    Support several pandas.read_csv parameters needed for the tests

    Args:
        filename: str, file name --> path is fixed
        header: how to set column names in df
        keep_default_na: how to handle standard na values in input
        na_values: possible additional values to read in as NaN
        index_col: use col as index

    Returns: pandas dataframe
    """
    filepath = os.path.join(TEST_RESOURCES_DIR, xml_file)
    tree = ET.parse(filepath)
    root = tree.getroot()
    xmlstr = ET.tostring(root, encoding="utf8", method="xml")
    return xmlstr


def init_moto_s3_bucket(bucket):
    """
    Initialise fake S3 bucket.

    Args:
        bucket: bucket name

    Returns: empty
    """
    conn = boto3.resource("s3", region_name=AWS_MOTO_REGION)
    conn.create_bucket(Bucket=bucket)


def init_moto_csv_s3(bucket, folder, infile, mock_name):
    """
    Initialise fake S3 with a CSV object.

    Args:
        bucket: bucket
        folder: folder
        infile: csv file to store in
        mock_name: S3 file object name

    Returns: empty
    """
    init_moto_s3_bucket(bucket)

    df = read_test_resource_csv(infile)
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False, sep=",", decimal=".")
    body = csv_buffer.getvalue()
    s3 = boto3.client("s3", region_name=AWS_MOTO_REGION)
    s3.put_object(Bucket=bucket, Key=f"{folder}/{mock_name}", Body=body)


def init_moto_json_s3(bucket, folder, infile, mock_name):
    """
    Initialise fake S3 with a JSON object.

    Args:
        bucket: bucket
        folder: folder
        infile: json file to store in
        mock_name: S3 file object name

    Returns: empty
    """
    init_moto_s3_bucket(bucket)

    jsn = read_test_resource_json(infile)
    body = bytes(json.dumps(jsn).encode("UTF-8"))
    s3 = boto3.client("s3", region_name=AWS_MOTO_REGION)
    s3.put_object(Bucket=bucket, Key=f"{folder}/{mock_name}", Body=body)


def init_moto_xml_s3(bucket: str, folder: str, xml_filename: str):
    """
    Initialise fake S3 with a CSV object.

    Args:
        bucket: bucket
        folder: folder
        xml_filename: S3 file object name

    Returns: empty
    """
    conn = boto3.resource("s3", region_name=AWS_MOTO_REGION)
    conn.create_bucket(Bucket=bucket)

    tree = read_test_resource_xml(xml_filename)
    s3 = boto3.client("s3", region_name=AWS_MOTO_REGION)
    s3.put_object(Bucket=bucket, Key=f"{os.path.join(folder)}/{xml_filename}", Body=tree)


def read_moto_s3_file(bucket: str, folder: str, filename: str):
    """Read a test file from the mocked S3 bucket."""
    s3 = boto3.client("s3", region_name=AWS_MOTO_REGION)
    file_body = s3.get_object(Bucket=bucket, Key=f"{os.path.join(folder)}/{filename}")["Body"]
    return file_body
