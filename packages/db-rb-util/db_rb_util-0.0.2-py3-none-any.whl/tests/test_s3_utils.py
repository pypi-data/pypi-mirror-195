"""Test s3 utility functions using moto."""
import os
from io import BytesIO, StringIO

import boto3
import pandas as pd
import pytest
from moto import mock_s3
from pandas.testing import assert_frame_equal

from db_rb_util import s3_utils
from tests.common_resources import (
    init_moto_csv_s3,
    init_moto_s3_bucket,
    read_moto_s3_file,
    read_test_resource_csv,
)


@mock_s3
def test_get_s3_bucket():
    """Check helper function that returns a bucket in a specified region."""
    bucketname = "testbucket"
    init_moto_s3_bucket(bucket=bucketname)

    bucket = s3_utils._get_s3_bucket(region_name="us-east-1", bucket_name=bucketname)
    assert bucket.name == "testbucket"


@mock_s3
def test_write_to_s3():
    """Test for writing to an S3 bucket."""
    region = "us-east-1"
    bucketname = "testbucket"
    foldername = "testfolder"
    filename = "testfile"
    init_moto_s3_bucket(bucket=bucketname)

    s3_utils.write_to_s3(
        file_buffer=BytesIO(b"test_text"),
        region=region,
        bucketname=bucketname,
        foldername=foldername,
        filename=filename,
    )
    body = read_moto_s3_file(bucket=bucketname, folder=foldername, filename=filename)

    assert body.read() == b"test_text"


@mock_s3
def test_move_s3_files_no_delete(tmp_path, mocker):
    """Test moving files in a s3 bucket, keeping the original."""
    mocker.patch(
        "tests.common_resources.read_test_resource_csv",
        return_value=pd.DataFrame(),
    )
    bucket = "my-test-bucket"
    region = "eu-central-1"
    testfilename = tmp_path / "test_file.csv"
    testfilename.touch()

    folder = "test/test_folder"
    folder_archive = folder + "/archive"

    init_moto_csv_s3(bucket=bucket, folder=folder, infile=testfilename, mock_name="test_file.csv")

    key = os.path.join(folder, "test_file.csv")
    key_archive = os.path.join(folder_archive, "test_file.csv")
    s3_utils.move_s3_file(bucket=bucket, region=region, key=key, archive_key=key_archive, do_delete=False)

    archive_body = read_moto_s3_file(bucket=bucket, folder=folder_archive, filename="test_file.csv")
    assert archive_body is not None
    org_body = read_moto_s3_file(bucket=bucket, folder=folder, filename="test_file.csv")
    assert org_body is not None


@mock_s3
def test_move_s3_files_with_delete(tmp_path, mocker):
    """Test moving files in a s3 bucket and deleting original."""
    mocker.patch(
        "tests.common_resources.read_test_resource_csv",
        return_value=pd.DataFrame(),
    )
    bucket = "my-test-bucket"
    region = "eu-central-1"
    testfilename = tmp_path / "test_file.csv"
    testfilename.touch()

    folder = "test/test_folder"
    folder_archive = folder + "/archive"

    init_moto_csv_s3(bucket=bucket, folder=folder, infile=testfilename, mock_name="test_file.csv")

    key = os.path.join(folder, "test_file.csv")
    key_archive = os.path.join(folder_archive, "test_file.csv")
    s3_utils.move_s3_file(bucket=bucket, region=region, key=key, archive_key=key_archive, do_delete=True)

    archive_body = read_moto_s3_file(bucket=bucket, folder=folder_archive, filename="test_file.csv")
    assert archive_body is not None
    with pytest.raises(Exception) as e:
        _ = read_moto_s3_file(bucket=bucket, folder=folder, filename="test_file.csv")
        assert str(e.value).find("NoSuchKey") > 0


@mock_s3
def test_write_pdf_to_s3():
    """Test for writing a pdf as a csv file to an S3 bucket."""
    bucket = "testbucket"
    # mock S3 bucket
    init_moto_s3_bucket(bucket=bucket)

    # write a dataframe to the bucket
    df_write = pd.DataFrame(
        data={
            "col1": [1, 2, 3, 4],
            "col2": [
                "text1",
                "text2",
                "text3",
                "text4",
            ],
        }
    )
    filename = "mytest.csv"
    folder = "testfolder"
    s3_utils.write_pdf_to_s3(df=df_write, region="us-east-1", bucketname=bucket, foldername=folder, filename=filename)

    # read it in again
    s3_obj = boto3.client("s3")
    s3_conn = s3_obj.get_object(Bucket=bucket, Key=f"{folder}/{filename}")
    df_read = pd.read_csv(filepath_or_buffer=BytesIO(s3_conn["Body"].read()), sep=",", index_col=None, header=0)

    assert_frame_equal(df_write, df_read)


@mock_s3
def test_read_from_s3():
    """Test for reading a file from s3."""
    bucket = "testbucket"
    region = "us-east-1"
    testfilename = "xml_variables_mapping_blanks.csv"
    folder = "test/test_folder"
    init_moto_csv_s3(bucket=bucket, folder=folder, infile=testfilename, mock_name=testfilename)

    bytes_data = s3_utils.read_from_s3(bucketname=bucket, region=region, filename="/".join([folder, testfilename]))

    df_read = pd.read_csv(
        filepath_or_buffer=BytesIO(bytes_data),
        sep=",",
        decimal=".",
        quotechar='"',
        encoding="utf-8",
        header=0,
        index_col=None,
    )

    df_exp = read_test_resource_csv(testfilename)

    assert_frame_equal(df_read, df_exp)


@mock_s3
def test_get_files_batch():
    """Test getting files from s3 with same extension."""
    bucket = "testbucket"
    region = "us-east-1"
    folder = "test"

    init_moto_s3_bucket(bucket)

    s3 = boto3.client("s3", region_name=region)
    s3.put_object(Bucket=bucket, Key=f"{folder}/testfile1.csv", Body=b"test_text")
    s3.put_object(Bucket=bucket, Key=f"{folder}/testfile2.csv", Body=b"test_text")

    files = s3_utils.get_files_batch(ext="csv", region=region, bucket_name=bucket, folder=folder)

    assert len(files) == 2

    files2 = s3_utils.get_files_batch(ext=".csv", region=region, bucket_name=bucket, folder=folder)

    assert len(files2) == 2

    no_files = s3_utils.get_files_batch(ext="txt", region=region, bucket_name=bucket, folder=folder)

    assert len(no_files) == 0


@mock_s3
def test_get_files_request():
    """Test getting files from s3 with specified prefix and suffix."""
    bucket = "testbucket"
    region = "us-east-1"
    folder = "test"

    init_moto_s3_bucket(bucket)

    s3 = boto3.client("s3", region_name=region)
    s3.put_object(Bucket=bucket, Key=f"{folder}/test_file_1.csv", Body=b"test_text")
    s3.put_object(Bucket=bucket, Key=f"{folder}/test_file_2.csv", Body=b"test_text")

    files_prefix = s3_utils.get_files_request(
        ext="csv", region=region, bucket_name=bucket, folder=folder, file_prefix="test", file_suffix="1"
    )

    assert len(files_prefix) == 1

    files_suffix = s3_utils.get_files_request(
        ext="csv", region=region, bucket_name=bucket, folder=folder, file_suffix="2"
    )

    assert len(files_suffix) == 1

    files_suffix2 = s3_utils.get_files_request(
        ext=".csv", region=region, bucket_name=bucket, folder=folder, file_suffix="1"
    )

    assert len(files_suffix2) == 1

    no_file = s3_utils.get_files_request(
        ext="csv", region=region, bucket_name=bucket, folder=folder, file_prefix="test", file_suffix="3"
    )

    assert len(no_file) == 0


@mock_s3
def test_get_files_file():
    """Test getting a particular file from s3."""
    bucket = "testbucket"
    region = "us-east-1"
    folder = "test"

    init_moto_s3_bucket(bucket)

    s3 = boto3.client("s3", region_name=region)
    s3.put_object(Bucket=bucket, Key=f"{folder}/test_file_1.csv", Body=b"test_text")
    s3.put_object(Bucket=bucket, Key=f"{folder}/test_file_2.csv", Body=b"test_text")

    file = s3_utils.get_files_file(region=region, bucket_name=bucket, filekey="test/test_file_2.csv")

    assert len(file) == 1
    assert file[0].key == "test/test_file_2.csv"


@mock_s3
def test_get_files_file_empty():
    """Test getting a particular file from s3."""
    bucket = "testbucket"
    region = "us-east-1"
    init_moto_s3_bucket(bucket)

    file = s3_utils.get_files_file(region=region, bucket_name=bucket, filekey="test/xml_variables_mapping_blanks.csv")

    assert file == []
