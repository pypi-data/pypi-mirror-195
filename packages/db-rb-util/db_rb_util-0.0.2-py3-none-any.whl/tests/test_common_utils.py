"""Test common utility functions."""
import os

import environs
import pandas as pd
import pytest
from environs import Env
from freezegun import freeze_time

from db_rb_util.common_utils import (
    _get_timestamp,
    get_timestamp_filename,
    try_fetch_env,
    write_df_to_csv,
)

envs = ["dev", "preprod", "prod"]
path = os.path.dirname(os.path.abspath(__file__))


@freeze_time("2023-01-01 00:00:00")
@pytest.mark.parametrize(
    "filename, datasource, extension, exp_filename, exp_extension",
    [
        ["test_filename", "coop", "ex", "coop_test_filename", ".ex"],
        ["test_filename.ex", "coop", "ex", "coop_test_filename", ".ex"],
        ["test_filename.", "coop", "ex", "coop_test_filename", ".ex"],
        ["test_filename", "coop", ".ex", "coop_test_filename", ".ex"],
        ["{datasource}_test_filename_{timestamp}", "coop", ".ex", f"coop_test_filename", ".ex"],
    ],
)
def test_get_timestamp_filename(filename, datasource, extension, exp_filename, exp_extension):
    """Check helper function that adds a timestamp to a filename."""
    timestamp = _get_timestamp()
    exp = f"{exp_filename}_{timestamp}{exp_extension}"

    assert get_timestamp_filename(name=filename, datasource=datasource, ext=extension) == exp
    assert get_timestamp_filename(name="", datasource=datasource, ext=extension) is None


def test_write_df_to_csv(caplog, tmp_path):
    """Check helper function that saves a dataframe to a csv with a given filename."""
    test_df = pd.DataFrame({"retailers": ["aldi", "lidl", "tesco"], "average_trip_cost": [80.25, 85.00, 120.5]})
    test_filename = "test.csv"
    exp_file = "retailers,average_trip_cost\naldi,80.25\nlidl,85.0\ntesco,120.5\n"
    path_temp = tmp_path / "test_src"
    path_temp.mkdir()
    write_df_to_csv(df=test_df, path=path_temp, filename=test_filename)

    with open(path_temp / test_filename, "r") as f:
        file = f.read()
    assert file == exp_file

    with pytest.raises(FileExistsError):
        write_df_to_csv(df=test_df, path="wrong_path", filename=test_filename)
    assert caplog.records[0].message == "wrong_path does not exist"


@pytest.mark.parametrize("env", ["dev", "preprod", "prod"])
def test_try_fetch_env(monkeypatch, env):
    """Test for fetching environment."""
    monkeypatch.setenv(name="DBS_ENV", value=env)
    assert try_fetch_env(config_env_key="DBS_ENV", envs=envs) == env


def test_try_fetch_env_from_env_file(tmp_path, mocker):
    """Test for fetching environment from .env file."""
    env_path = tmp_path / ".env"
    env_path.touch()
    with open(env_path, "w") as test_file:
        test_file.write("DBS_ENV=dev")

    assert try_fetch_env(config_env_key="DBS_ENV", envs=envs, path=env_path) == "dev"


def test_try_fetch_env_error(caplog, monkeypatch):
    """Test for error handling of fetching environment function."""
    with pytest.raises(environs.EnvValidationError) as pytest_wrapped_e:
        monkeypatch.setenv(name="DBS_ENV", value="")  # wrong_env
        try_fetch_env(config_env_key="DBS_ENV", envs=envs)

    exp_message = """Environment variable "DBS_ENV" invalid: ["DBS_ENV must be one of: ['dev', 'preprod', 'prod']"]"""

    assert exp_message in str(pytest_wrapped_e.value)
    assert caplog.records[0].message == exp_message
