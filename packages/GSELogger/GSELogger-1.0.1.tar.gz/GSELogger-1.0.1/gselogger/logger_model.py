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
import os
from sys import platform
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Optional


class LoggerModel:
    """Model for creating logging backend for an application."""

    def __init__(
            self,
            app_name: str,
            filename: Optional[str] = "",
            filepath: Optional[str] = "",
            overwrite_logs: Optional[bool] = False
    ) -> None:
        # Set the fullpath of the log file
        fullpath = self._create_log_fullpath(filename=filename, filepath=filepath, app_name=app_name)
        # Set the filemode value based on user input. Overwrite with "w" and append with "a"!
        filemode = "w" if overwrite_logs else "a"
        # Set logging configuration
        logging.basicConfig(
            filename=fullpath,
            level=logging.INFO,
            filemode=filemode,
            format="%(asctime)s | %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]"
        )

    @staticmethod
    def _create_log_fullpath(filename: str, filepath: str, app_name: str) -> str:
        """
        Creates the logfile path based on input and operating system
        :return: Returns the complete logfile path as posix.
        """

        # Set the filename
        if filename == "":
            filename = app_name
        filename += ".log"

        if filepath == "":
            if platform.startswith("linux"):
                # Creates the path for linux based OS
                filepath = PurePosixPath(Path.home().joinpath(".local/share/")).joinpath(app_name).as_posix()
            elif platform.startswith("win32"):
                # Creates the path for Windows based OS
                filepath = PureWindowsPath(os.getenv("APPDATA")).joinpath(app_name).as_posix()
            else:
                # Creates the path other OS
                filepath = Path.home().joinpath(app_name).as_posix()

        # Create the path if it doesn't exist
        filepath = Path(filepath)
        if not filepath.exists():
            filepath.mkdir(parents=True)

        # Add the filename to the path
        fullpath = filepath.joinpath(filename).as_posix()

        return fullpath

    @staticmethod
    def _check_file_path(filepath: str) -> Path:
        """Checks if the filepaths exists, and creates one if it doesn't."""
        filepath = Path(filepath)
        if not filepath.exists():
            filepath.mkdir(parents=True)
        return filepath

    @staticmethod
    def _create_log_message(message: str, exception_type: str) -> str:
        """Returns the formatted log message, including exception type if available."""
        return f"{exception_type}: {message}" if exception_type != "" else message

    @staticmethod
    def info(message: str) -> None:
        """Creates an info log message"""
        logging.info(f"INFO     | {message}")

    def warning(self, message: str, exception_type: Optional[str] = "") -> None:
        """Creates a warning log message"""
        logging.warning(f"WARNING  | {self._create_log_message(message, exception_type)}")

    def error(self, message: str, exception_type: Optional[str] = "") -> None:
        """Creates an error log message"""
        logging.error(f"ERROR    | {self._create_log_message(message, exception_type)}")

    def critical(self, message: str, exception_type: Optional[str] = "") -> None:
        """Creates a critical log message"""
        logging.critical(f"CRITICAL | {self._create_log_message(message, exception_type)}")
