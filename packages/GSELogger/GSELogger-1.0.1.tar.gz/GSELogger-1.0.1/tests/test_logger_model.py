#!/usr/bin/python3
# ----------------------------------------------------------------------
# GSELogger - Python logging model for any python application.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2023  GSECARS, The University of Chicago, USA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import logging
import pytest
from pathlib import Path

from gselogger.logger_model import LoggerModel


@pytest.fixture
def test_log_directory(tmp_path) -> None:
    """Create temporary directory for test logs."""
    log_directory = tmp_path / "logs"
    log_directory.mkdir()
    yield log_directory
    for file in log_directory.glob("*"):
        file.unlink()
    log_directory.rmdir()


@pytest.fixture
def logger(test_log_directory) -> LoggerModel:
    """Create logger instance to use for testing."""
    logging.getLogger().setLevel(logging.INFO)
    return LoggerModel(app_name="TestApplication", filepath=test_log_directory)


def test_create_log_fullpath_with_filepath() -> None:
    """Test creating fullpath with a specified filepath and application name."""
    fullpath = LoggerModel._create_log_fullpath(
        filename="",
        filepath=Path.home().joinpath("TestApplication").as_posix(),
        app_name="TestApplication"
    )

    # Create the filepath
    expected_path = Path.home().joinpath("TestApplication").joinpath("TestApplication.log").as_posix()
    # Check the filepath
    assert fullpath == expected_path


def test_create_log_fullpath_with_filename_and_filepath() -> None:
    """Test creating fullpath with filename, filepath and application name specified."""
    fullpath = LoggerModel._create_log_fullpath(
        filename="Application",
        filepath=Path.home().joinpath("TestApplication").as_posix(),
        app_name="TestApplication"
    )

    # Create the filepath
    expected_path = Path.home().joinpath("TestApplication").joinpath("Application.log").as_posix()
    # Check the filepath
    assert fullpath == expected_path


def test_logger_info(logger: LoggerModel, caplog: pytest.LogCaptureFixture) -> None:
    """Test the logging info method."""
    message = "Test message"
    logger.info(message)
    assert "INFO" in caplog.text
    assert message in caplog.text


def test_logger_warning(logger: LoggerModel, caplog: pytest.LogCaptureFixture) -> None:
    """Test the logging warning method."""
    message = "Test message"
    exception_type = "TestException"
    logger.warning(message, exception_type)
    assert "WARNING" in caplog.text
    assert message in caplog.text
    assert exception_type in caplog.text


def test_logger_error(logger: LoggerModel, caplog: pytest.LogCaptureFixture) -> None:
    """Test the logging error method."""
    message = "Test message"
    exception_type = "TestException"
    logger.error(message, exception_type)
    assert "ERROR" in caplog.text
    assert message in caplog.text
    assert exception_type in caplog.text


def test_logger_critical(logger: LoggerModel, caplog: pytest.LogCaptureFixture) -> None:
    """Test the logging critical method."""
    message = "Test message"
    exception_type = "TestException"
    logger.critical(message, exception_type)
    assert "CRITICAL" in caplog.text
    assert message in caplog.text
    assert exception_type in caplog.text
