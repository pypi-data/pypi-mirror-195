"""Classes for connecting to rds and mongodb databases."""
import json
import os

import boto3
import pymongo as pm
import sqlalchemy


class DBConnector:
    """Super class for database connection to hold common methods."""

    def __init__(self):
        """Initialize for DBConnector."""
        self.db = None
        self.engine = None

    def set_db(self, name):
        """Set db name."""
        self.db = name
        return self

    def set_engine(self):
        """Set engine."""
        conn_str = self.get_connection_string()
        eng = sqlalchemy.create_engine(conn_str)
        self.engine = eng
        return self

    def get_engine(self):
        """Retrieve engine."""
        return self.engine

    def get_connection_string(self):
        """Retrieve connection string."""
        pass


class MongoDBConnector:
    """Class for MongoDB."""

    def __init__(self, *, database: str, collection: str, region: str, arn_params: str, arn_secrets: str):
        """
        Initialise MongoDB connector.

        Args:
            database (str): The database to connect to.
            collection (str): The collection within the database the data will be taken from.
            region (str): AWS region name
            arn_params (str): ARN parameters to access the connections credentials on Secrets Manager.
            arn_secrets (str): ARN secret to access the connections credentials on Secrets Manager.

        """
        self.db = database
        self.col = collection
        self.username = ""
        self.password = ""
        self.host = ""
        self.client = None
        self.region_name = region
        self.cluster_arn_parameter_name = arn_params
        self.secret_arn_parameter_name = arn_secrets
        self.cluster_arn = None
        self.secret_arn = None

    def set_arns(self):
        """Set arns parameters."""
        self.cluster_arn = os.environ.get(self.cluster_arn_parameter_name)
        self.secret_arn = os.environ.get(self.secret_arn_parameter_name)
        return self

    def get_secret_values(self):
        """Get secret values."""
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=self.region_name)
        secret_response = client.get_secret_value(SecretId=self.secret_arn)
        secret_string = secret_response["SecretString"]
        secret_values = json.loads(secret_string)
        return secret_values

    def set_password_username(self):
        """Set the password and username to connect to MongoDB."""
        secrets = self.get_secret_values()
        self.username = secrets["username"]
        self.password = secrets["password"]
        self.host = secrets["uri"]
        return self

    def set_client(self):
        """Connect to MongoDB using the credentials and the uri."""
        mongo_client = pm.MongoClient(
            username=self.username,
            password=self.password,
            host=self.host,
            authSource=self.db,
        )
        self.client = mongo_client
        return self

    def get_client(self):
        """Get the MongoDB client."""
        return self.client
