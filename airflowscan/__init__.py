# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Nightwatch Cybersecurity.
#
# This file is part of airflowscan
# (see https://github.com/nightwatchcybersecurity/airflowscan).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import json

import anymarkup
from configobj import ConfigObj
from jsonschema.validators import validator_for

__version__ = '0.1.0'
DEFAULT_FILE = 'data/default_airflow.cfg'
HARDENED_FILE = 'data/hardened_airflow.cfg'
SCHEMA_FILE = 'data/airflow_cfg.schema'

class ValidationError(object):
    """
    Represents a schema validation error.
    Note that 'setting' maybe None for error originating at the section level.
    """
    def __init__(self, title, section, setting, message):
        self.title = title
        self.section = section
        self.setting = setting
        self.message = message


class Utils(object):
    """Various utility functions, split from the main class for ease of unit testing"""

    @staticmethod
    def _load_schema():
        """
        Loads schema data from disk and converts to a JSON dictionary

        :return: JSON dictionary
        """
        schema_file = open(SCHEMA_FILE, 'r')
        schema_data = json.load(schema_file)
        return schema_data

    @staticmethod
    def _convert_config_file_to_json_dict(filename):
        """
        Parses the provided file to a dictionary then converts to JSON then to dictionary.
        Needs to do a double trip because the anymarkup module autoconverts booleans and integers.

        :param filename: filename to convert
        :return: JSON data as a dictionary
        """
        config = ConfigObj(filename, interpolation=False, list_values=False)
        dict_data = config.dict()
        json_data = json.dumps(dict_data)
        json_dict = anymarkup.parse(json_data)
        return json_dict

    @staticmethod
    def validate(filename):
        """
        Validates provided JSON dictionary based on our schema

        :param filename: file to be validated
        :return: list of errors
        """

        # Load schema and initialize validator
        schema_data = Utils._load_schema()
        validator = validator_for(schema_data)

        # Read file, convert to a JSON dictionary and validate
        data = Utils._convert_config_file_to_json_dict(filename)
        errors = validator(schema=schema_data).iter_errors(data)

        # Convert errors to our own class
        data = []
        for error in errors:
            data.append(ValidationError(
                title=error.schema['title'],
                section=error.path[0],
                setting=error.path[1] if len(error.path) > 1 else None,
                message=error.message
            ))
        return data
