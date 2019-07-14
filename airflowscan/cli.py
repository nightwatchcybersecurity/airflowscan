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
import json, sys

import anymarkup
import click
from configobj import ConfigObj
from jsonschema.validators import validator_for

from airflowscan.utils import Utils


@click.version_option(version=Utils.get_version(), prog_name='airflowscan')
@click.group()
def cli():
    """
    airflowscan - Static analysis tool to check Airflow configuration files for insecure settings.

    Copyright (c) 2019 Nightwatch Cybersecurity.
    Source code: https://github.com/nightwatchcybersecurity/airflowscan
    """


@cli.command('scan')
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def scan(filename):
    """Scan an Airflow configuration file ('airflow.cfg')"""

    # Parse the provided file to a dictionary then convert to JSON
    config = ConfigObj(filename, interpolation=False, list_values=False)
    dict_data = config.dict()
    json_data = json.dumps(dict_data)
    data_to_check = anymarkup.parse(json_data)

    # Load schema file
    schema_file = open('data/airflow_cfg.schema', 'r')
    schema_data = json.load(schema_file)

    # Validate using JsonSchema
    validator = validator_for(schema_data)
    errors = validator(schema=schema_data).iter_errors(data_to_check)
    for error in errors:
        click.echo(error.schema['title'])
        if len(error.path) == 1:
            click.echo('Section [' + error.path[0] + ']: ' + error.message)
        else:
            click.echo('Section [' + error.path[0] + '], setting "' + error.path[1] + '": ' + error.message)
        click.echo()

    # Return error
    if errors:
        exit(1)


if __name__ == '__main__':
    cli()