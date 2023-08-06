"""Utility functions to connect, read and write to mongodb."""

from collections.abc import MutableMapping
from typing import Any, Optional, Union

from bson.raw_bson import RawBSONDocument
from pymongo import MongoClient
from pymongo.collection import Collection

from db_rb_util.db_connector import MongoDBConnector
from db_rb_util.logging_utils import get_logger

logger = get_logger("db_logger")


def get_mongo_db_connector(
    database: str, collection: str, region: str, arn_params: str, arn_secrets: str
) -> MongoClient:
    """
    Connect to MongoDB.

    Args:
        database (str): The database to connect to.
            collection (str): The collection within the database the data will be taken from.
            region (str): AWS region name
            arn_params (str): ARN parameters to access the connections credentials on Secrets Manager.
            arn_secrets (str): ARN secret to access the connections credentials on Secrets Manager.

    Returns:
        mongodb client
    """
    try:
        db_connector = (
            MongoDBConnector(
                database=database, collection=collection, region=region, arn_params=arn_params, arn_secrets=arn_secrets
            )
            .set_arns()
            .set_password_username()
        )
        client = db_connector.set_client().get_client()
        client_info = client.server_info()
        logger.info(f"Successfully connected to MongoDB on {client.address}")
        logger.info(f"MongoDB server information {str(client_info)}")
    except Exception as e:
        logger.error(f"Unable to connect to MongoDB : {str(e)}")
        client = None
        raise e
    return client


def get_documents(collection: Collection, item_filter: dict, projection: dict) -> list[dict]:
    """
    Get the list of documents in MongoDB matching the filter and then apply the specific query.

    Args:
        collection (pm.collection.Collection): The collection in which we are querying the documents.
        item_filter (dict): Filter that specifies the fields in documents that should be matched.
        projection (dict): Specifies which field names should be included in the result set.

    Returns:
        The list of documents matching the filter and containing the fields specified by projection.
    """
    try:
        cursor = collection.find(filter=item_filter, projection=projection)
        documents = list(cursor)

    except Exception as e:
        logger.error(f"Invalid query to MongoDB : {str(e)}")
        raise e

    return documents


def get_document(collection: Collection, item_filter: dict, projection: dict) -> Optional[dict]:
    """
    Get one document in MongoDB matching the filter and then apply the specific query.

    Args:
        collection (pm.collection.Collection): The collection in which we are querying the documents.
        item_filter (dict): Filter that specifies the fields in documents that should be matched.
        projection (dict): Specifies which field names should be included in the result set.

    Returns:
        The list of documents matching the filter and containing the fields specified by projection.
    """
    try:
        cursor = collection.find_one(filter=item_filter, projection=projection)
        document = cursor

    except Exception as e:
        logger.error(f"Invalid query to MongoDB : {str(e)}")
        raise e

    return document


def get_documents_aggregation(collection: Collection, pipeline: list[dict]) -> list[dict]:
    """
    Execute an aggregation operation using the pipeline.

    Args:
        collection (pm.collection.Collection): The collection in which we are performing the aggregation.
        pipeline (list[dict]): List of aggregation operations to execute.

    Returns:
        List of documents resulting from this aggregation pipeline.
    """
    try:
        cursor = collection.aggregate(pipeline)
        documents = list(cursor)

    except Exception as e:
        logger.error(f"Something went wrong with your pipeline : {str(e)}")
        raise e

    return documents


def save_to_mongodb(collection: Collection, input_data: Union[MutableMapping[str, Any], RawBSONDocument]):
    """
    Save data to mongo db collection.

    Args:
        collection (pm.collection.Collection): The collection to save to.
        input_data (str): json message via SQS

    Returns:
          empty
    """
    try:
        insert_id = collection.insert_one(input_data)
        logger.info(f"Records inserted in the data base: {insert_id} records")

    except Exception as e:
        logger.error(f"Something went wrong : {str(e)}")
        raise e


def update_document_value(collection: Collection, filter: dict, update_set: dict):
    """
    Get the documents in MongoDB matching the filter and then update one item specific query.

    Args:
        collection (pm.collection.Collection): The collection in which we are querying the documents.
        filter (dict): Filter that specifies the fields in documents that should be matched.
        update_set (dict): field names of the to be updated fields and their values

    Returns:
        empty
    """
    try:
        collection_name = collection.name
        field_names = update_set.keys
        collection.update_one(filter, {"$set": update_set})
        logger.info(f"Updated '{collection_name}' text collection: {field_names}")

    except Exception as e:
        logger.error(f"Invalid query to MongoDB : {str(e)}")
        raise e
