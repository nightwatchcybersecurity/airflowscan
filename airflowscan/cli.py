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
import sys

import click

from airflowscan import Utils, __version__ as version


@click.version_option(version=version, prog_name='airflowscan')
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

    # Get validation errors
    errors = Utils.validate(filename)

    # Display results to the user
    for error in errors:
        click.echo(error.title)
        if error.setting:
            click.echo('Section [' + error.section + '], setting "' + error.setting + '": ' + error.message + "\n")
        else:
            click.echo('Section [' + error.section + ']: ' + error.message + "\n")

    # Return error
    if len(errors) > 0:
        click.echo("Total validation errors found: " + str(len(errors)))
        exit(1)


if __name__ == '__main__':
    cli()