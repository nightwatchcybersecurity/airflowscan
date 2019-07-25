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
from airflowscan import Utils, HARDENED_FILE, DEFAULT_FILE
from anymarkup import AnyMarkupError
import pytest


class TestUtils(object):
    def test_load_schema(self):
        schema_data = Utils._load_schema()
        properties = schema_data['properties']

        assert len(properties['admin']) > 0
        assert len(properties['api']) > 0
        assert len(properties['celery']) > 0
        assert len(properties['core']) > 0
        assert len(properties['dask']) > 0
        assert len(properties['ldap']) > 0
        assert len(properties['scheduler']) > 0
        assert len(properties['smtp']) > 0
        assert len(properties['webserver']) > 0

    def test_convert_config_file_to_json_dict_file_doesnt_exist(self):
        with pytest.raises(AnyMarkupError):
            Utils._convert_config_file_to_json_dict('foobar')

    def test_convert_config_file_to_json_dict(self):
        data = Utils._convert_config_file_to_json_dict(HARDENED_FILE)
        assert type(data) == dict
        assert len(data) > 0
        assert type(data['core']['logging_level']) == str
        assert data['core']['logging_level'] == 'INFO'

    def test_convert_config_file_to_json_dict_valid_file_booleans_as_bool(self):
        data = Utils._convert_config_file_to_json_dict(HARDENED_FILE)
        assert type(data) == dict
        assert len(data) > 0
        assert len(data) > 0
        assert type(data['core']['remote_logging']) == bool
        assert data['core']['remote_logging'] is False

    def test_convert_config_file_to_json_dict_arrays_as_str(self):
        data = Utils._convert_config_file_to_json_dict(HARDENED_FILE)
        assert type(data) == dict
        assert len(data) > 0
        assert type(data['celery']['flower_basic_auth']) == list
        assert len(data['celery']['flower_basic_auth']) == 2

    def test_validate_default_file(self):
        data = Utils.validate(DEFAULT_FILE)
        assert len(data) == 31

    def test_validate_hardened_file(self):
        data = Utils.validate(HARDENED_FILE)
        assert len(data) == 0
