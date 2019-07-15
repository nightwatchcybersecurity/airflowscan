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
from airflowscan import  __version__ as version, HARDENED_FILE, DEFAULT_FILE
from airflowscan.cli import cli
from click.testing import CliRunner
import pytest


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


class TestCli():
    def test_no_arguments(self, runner):
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert not result.exception

    def test_invalid_command(self, runner):
        result = runner.invoke(cli, ['--foobar'])
        assert result.exit_code != 0
        assert result.exception

    def test_help(self, runner):
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert not result.exception

    def test_scan_help(self, runner):
        result = runner.invoke(cli, ['scan', '--help'])
        assert result.exit_code == 0
        assert not result.exception

    def test_version(self, runner):
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert not result.exception
        assert result.output == 'airflowscan, version ' + version + '\n'

    def test_scan_invalid_file(self, runner):
        result = runner.invoke(cli, ['scan', 'foobar'])
        assert result.exit_code == 2
        assert result.exception

    def test_scan_default_file(self, runner):
        result = runner.invoke(cli, ['scan', DEFAULT_FILE])
        assert result.exit_code == 1
        assert result.exception

    def test_scan_hardened_file(self, runner):
        result = runner.invoke(cli, ['scan', HARDENED_FILE])
        assert result.exit_code == 0
        assert not result.exception