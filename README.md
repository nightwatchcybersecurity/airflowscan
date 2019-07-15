# airflowscan
[![PyPI version](https://badge.fury.io/py/airflowscan.svg)](https://badge.fury.io/py/airflowscan)
[![Build Status](https://travis-ci.org/nightwatchcybersecurity/airflowscan.svg?branch=master)](https://travis-ci.org/nightwatchcybersecurity/airflowscan)
[![codecov](https://codecov.io/gh/nightwatchcybersecurity/airflowscan/branch/master/graph/badge.svg)](https://codecov.io/gh/nightwatchcybersecurity/airflowscan)
![GitHub](https://img.shields.io/github/license/nightwatchcybersecurity/airflowscan.svg)
Checklist and tools for increasing security of Apache Airflow.
 
## DISCLAIMER
This project NOT AFFILIATED with the Apache Foundation and the Airflow project,
and is not endorsed by them. 

## Contents
The purpose of this project is provide tools to increase security of
[Apache Airflow](https://airflow.apache.org/). 
installations. This projects provides the following tools:
- Configuration file with hardened settings - see [hardened_airflow.cfg](data/hardened_airflow.cfg).
- Security checklist for hardening default installations - see [CHECKLIST.MD](data/CHECKLIST.md).
- Static analysis tool to check Airflow configuration files for insecure settings.
- JSON schema document used for validation by the static analysis tool - see [airflow_cfg.schema](data/airflow_cfg.schema)  

# Information for the Static Analysis Tool (airflowscan)
The static analysis tool can check an Airflow configuration file for settings related to security. The tool
convers the config file to JSON, and then uses a JSON Schema to do the validation.

## Requirements
Python 3 is required and you can find all required modules in the **requirements.txt** file.
Only tested on Python 3.7 but should work on other 3.x releases. No plans to 2.x support at
this time.

## Installation
You can install this via PIP as follows:
```
pip install airflowscan
airflowscan
```
To download and run manually, do the following:
```
git clone https://github.com/nightwatchcybersecurity/airflowscan.git
cd airflowscan
pip -r requirements.txt
python -m airflowscan.cli
```

## How to use 
To scan a configuration file, do the following command:
```
airflowscan scan some_airflow.cfg
```

# Reporting bugs and feature requests
Please use the GitHub issue tracker to report issues or suggest features:
https://github.com/nightwatchcybersecurity/airflowscan

You can also send emai to ***research /at/ nightwatchcybersecurity [dot] com***
