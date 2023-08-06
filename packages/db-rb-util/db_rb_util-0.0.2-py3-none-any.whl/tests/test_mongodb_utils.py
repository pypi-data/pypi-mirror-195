"""Test MongoDB utility functions using mongomock."""
import json

import mongomock
import pytest
from bson.json_util import dumps

from db_rb_util.mongodb_utils import (
    get_document,
    get_documents,
    get_documents_aggregation,
    get_mongo_db_connector,
    save_to_mongodb,
    update_document_value,
)


@mongomock.patch()
def test_get_mongodb_connector(mocker):
    """Check helper function that connects to a MongoDB server."""
    database = "test_db"
    collection = "test_collection"
    region = "eu-central-1"
    arn_params = "arn_mongodb"
    arn_secrets = "arn_mongodb_secret"
    mocker.patch(
        "db_rb_util.db_connector.MongoDBConnector.get_secret_values",
        return_value={"username": "", "password": "", "uri": ""},
    )
    client = get_mongo_db_connector(
        database=database, collection=collection, region=region, arn_params=arn_params, arn_secrets=arn_secrets
    )

    assert client.server_info()["ok"]


def test_get_mongo_db_connector_error():
    """Check error handling of helper function that connects to a MongoDB server."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        get_mongo_db_connector(database="", collection="", region="", arn_params="", arn_secrets="")

    assert (
        str(pytest_wrapped_e)
        == "<ExceptionInfo ValueError('Invalid endpoint: https://secretsmanager..amazonaws.com') tblen=11>"
    )


def test_get_documents():
    """Check helper function that fetches a list of document on MongoDB."""
    mock_client = mongomock.MongoClient()
    object = [{"text_id": 11, "value": 1}, {"text_id": 11, "value": 2}]

    for obj in object:
        obj["_id"] = mock_client.test_db.test_collection.insert_one(obj).inserted_id

    item_filter = {"text_id": 11}
    projection = {"text_id": 1, "value": 1}
    calc = get_documents(mock_client.test_db.test_collection, item_filter=item_filter, projection=projection)
    mock_client.close()
    assert type(calc) is list
    assert len(calc) == 2
    assert calc == object


def test_get_documents_error():
    """Check error handling of helper function that fetches a list of document on MongoDB."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        get_documents("", item_filter="", projection="")

    assert str(pytest_wrapped_e) == "<ExceptionInfo TypeError('find() takes no keyword arguments') tblen=3>"


def test_get_document():
    """Check helper function that fetches a document on MongoDB."""
    mock_client = mongomock.MongoClient()
    object = [{"test": 21, "test2": 1}, {"test": 21, "test2": 2}]

    for obj in object:
        obj["_id"] = mock_client.test_db.test_collection.insert_one(obj).inserted_id

    item_filter = {"test2": 2}
    projection = {"test": 1, "test2": 1}
    calc = get_document(mock_client.test_db.test_collection, item_filter=item_filter, projection=projection)
    mock_client.close()
    assert calc == object[1]


def test_get_document_error():
    """Check error handling of helper function that fetches a document on MongoDB."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        get_document(object, item_filter={}, projection={})

    assert (
        str(pytest_wrapped_e)
        == """<ExceptionInfo AttributeError("type object 'object' has no attribute 'find_one'") tblen=3>"""
    )


def test_get_documents_aggregation():
    """Check helper function that returns a list of documents based on an aggregation pipeline."""
    mock_client = mongomock.MongoClient()
    test_data = [
        {
            "retailerProductGroup": "Drikke",
            "productName": "Faxe Kondi",
            "description": "1,50 l",
            "totalPrice": 31,
            "discount": 0,
            "quantity": 2,
            "price": 15.5,
        },
        {
            "retailerProductGroup": "Drikke",
            "productName": "Imaginary product",
            "description": "20 x 0,33 l",
            "totalPrice": 156,
            "discount": 0,
            "quantity": 2,
            "price": 78,
        },
        {
            "retailerProductGroup": "Drikke",
            "productName": "Hello there",
            "description": "18 x 0,33 l",
            "totalPrice": 95,
            "discount": 13,
            "quantity": 1,
            "price": 95,
        },
        {
            "retailerProductGroup": "Drikke",
            "productName": "General Kenobi",
            "description": "170 g",
            "totalPrice": 21.75,
            "discount": 0,
            "quantity": 1,
            "price": 21.75,
        },
        {
            "retailerProductGroup": "Kiosk",
            "productName": "PANT",
            "description": "140 g",
            "totalPrice": 20.25,
            "discount": 0,
            "quantity": 1,
            "price": 20.25,
        },
    ]

    mock_client.test_db.test_collection.insert_many(test_data)

    pipeline_test = [
        {"$match": {"retailerProductGroup": "Drikke"}},
        {"$sort": {"price": 1}},
        {"$project": {"_id": 0, "productName": 1}},
    ]

    calc = get_documents_aggregation(mock_client.test_db.test_collection, pipeline=pipeline_test)

    exp = [
        {"productName": "Faxe Kondi"},
        {"productName": "General Kenobi"},
        {"productName": "Imaginary product"},
        {"productName": "Hello there"},
    ]
    mock_client.close()
    assert exp == calc


def test_get_documents_aggregation_error():
    """Check error handling of helper function that returns a list of documents based on an aggregation pipeline."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        get_documents_aggregation(object, pipeline=[{}])

    assert (
        str(pytest_wrapped_e)
        == """<ExceptionInfo AttributeError("type object 'object' has no attribute 'aggregate'") tblen=3>"""
    )


def test_save_to_mongodb():
    """Check helper function that saves a document to MongoDB."""
    mock_client = mongomock.MongoClient()
    test_data = {
        "ean": "0000000000000",
        "retailer": "REWE",
        "receipt_text_raw": "BEDIENUNGSTHEKE",
        "ean_rawtext_comb_nr": 1.0,
        "min_price": 590.0,
        "max_price": 882.0,
        "country": "DE",
    }
    test_data_1 = {
        "ean": "0000000000001",
        "retailer": "REWE",
        "receipt_text_raw": "BEDIENUNGSTHEKE",
        "ean_rawtext_comb_nr": 1.0,
        "min_price": 590.0,
        "max_price": 882.0,
        "country": "DE",
    }
    mock_client.test_db.test_collection.insert_one(test_data)
    save_to_mongodb(mock_client.test_db.test_collection, test_data_1)

    response = mock_client.test_db.test_collection.find_one({"ean": "0000000000001"})
    response = json.loads(dumps(response))

    oid_1 = test_data_1.get("_id")
    oid_2 = mongomock.ObjectId(response["_id"]["$oid"])

    assert oid_1 == oid_2

    test_data_1.pop("_id", None)
    response.pop("_id", None)
    mock_client.close()
    assert test_data_1 == response


def test_save_to_mongodb_error():
    """Check error handling of helper function that saves a document to MongoDB."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        save_to_mongodb(object, input_data=[])

    assert (
        str(pytest_wrapped_e)
        == """<ExceptionInfo AttributeError("type object 'object' has no attribute 'insert_one'") tblen=3>"""
    )


def test_update_document_value():
    """Check helper function that updates value in mongoDB."""
    mock_client = mongomock.MongoClient()
    test_object = [{"test": 1, "test2": 1}, {"test": 2, "test2": 2}]

    for obj in test_object:
        obj["_id"] = mock_client.test_db.test_collection.insert_one(obj).inserted_id

    filter = {"test": 1}
    update = {"test2": 10}
    update_document_value(mock_client.test_db.test_collection, filter=filter, update_set=update)
    calc = mock_client.test_db.test_collection.find_one({"test": 1})
    mock_client.close()
    assert calc["_id"] == test_object[0]["_id"]
    assert calc["test"] == test_object[0]["test"]
    assert calc["test2"] == 10 and test_object[0]["test2"] == 1


def test_update_document_value_error():
    """Check error handling of helper function that updates value in mongoDB."""
    with pytest.raises(Exception) as pytest_wrapped_e:
        update_document_value(object, filter={}, update_set={})

    assert (
        str(pytest_wrapped_e)
        == """<ExceptionInfo AttributeError("type object 'object' has no attribute 'name'") tblen=3>"""
    )
