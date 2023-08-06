"""Common utility functions for writing and naming files, in addition to fetching the environment and configuration."""
import os
from time import gmtime, strftime
from typing import Dict, Optional

import pandas as pd
import yaml  # type: ignore
from environs import Env, EnvError, EnvValidationError
from marshmallow.validate import OneOf

import db_rb_util.logging_utils as logging

logger = logging.get_logger("db_logger")

__pdoc__ = {"_get_timestamp": True}


def _get_timestamp() -> str:
    """
    Create timestamp string for unique filenames.

    Returns: str
    """
    timestamp_str = "{0}t{1}".format(strftime("%Y%m%d", gmtime()), strftime("%H%M", gmtime()))
    return timestamp_str


def get_timestamp_filename(*, name: str, datasource: str, ext: str) -> Optional[str]:
    """
    Add timestamp to filename.

    Args:
        name: filename passed by user
        ext: target file_all extension
        datasource: datasource name (receipt or rewe)

    Returns: str, filename with timestamp
    """
    if name == "":
        return None

    if name.endswith(ext):
        name = name[: -len(ext)]
    if name.endswith("."):
        name = name[:-1]
    if ext.startswith("."):
        ext = ext[1:]
    if "{datasource}" in name and "{timestamp}" in name:
        return f"{name}.{ext}".format(**{"datasource": datasource, "timestamp": _get_timestamp()})
    else:
        return f"{datasource}_{name}_{_get_timestamp()}.{ext}"


def write_df_to_csv(
    *,
    df: pd.DataFrame,
    path: str,
    filename: str,
    has_header: bool = True,
    has_index: bool = False,
    delimiter: str = ",",
    decimal: str = ".",
    quotechar: str = '"',
    encoding: str = "utf-8",
):
    """
    Take a pandas dataframe and writes it to a file with filename on the local machine.

    By default we have utf-8 encoding, double quotation marks and a period for decimal formatting.

    Args:
        df: pandas dataframe
        path (str): path on local machine
        filename (str):  filename
        has_header: export column names as header line
        has_index: export index as first columm
        delimiter (str): csv delimiter character/s
        decimal (str): character for decimals, "." by default
        quotechar (str): character for quotes, '"' by default
        encoding (str): data encoding, utf-8 by default


    Returns:
        None
    """
    if not os.path.exists(path):
        logger.error("%s does not exist", path)
        raise FileExistsError

    df.to_csv(
        os.path.join(path, filename),
        sep=delimiter,
        decimal=decimal,
        quotechar=quotechar,
        encoding=encoding,
        header=has_header,
        index=has_index,
    )


def try_fetch_env(config_env_key, envs, path=".env") -> Optional[str]:
    """
    Ensure the environment variable describing environment is present and matches possible values.

    Supports using an .env file for setting environment variables.

    Args:
        config_env_key (str): environment key, e.g. DBS_ENV
        envs (list): all environment options, e.g. ['dev', 'preprod', 'prod']
        path (str): path of .env file, default is source directory

    Returns: env key as string
    """
    try:
        env = Env()
        env.read_env(path=path)
        try:
            env.str(config_env_key, validate=OneOf(choices=envs, error=f"{config_env_key} must be one of: {envs}"))
            rms_env = os.environ[config_env_key]
        except EnvValidationError as e:
            logger.error(str(e))
            raise e
    except EnvError as e:
        logger.error(f"Missing {config_env_key} environment variable in execution environment. Exception {str(e)}")
        raise e

    return rms_env


def get_config_yaml(*, config_file: str, env: Optional[str]) -> Dict:
    """
    Load the config.yaml file as text file and returns the configuration for the respective environment.

    env in [preprod, prod]

    Args:
        config_file: filename of config file
        env (str): name of environment, preprod or prod

    Returns:
        dict, the config.yaml file
    """
    config = {}
    try:
        with open(config_file) as f:
            yaml_txt = f.read()
            config = yaml.safe_load(yaml_txt)
            config = config["environments"][env]
    except Exception as e:
        logger.error("Exception occurred during execution, traceback is %s", e)
    return config
