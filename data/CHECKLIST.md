# Airflow Security Checklist

## About
Checklist of security controls to secure your [Apache Airflow](https://airflow.apache.org/) installation since ["by default all gates are opened"](https://airflow.apache.org/security.html).


## Versions Targeted
This checklist covers the following versions:
   * 1.10.x

# Checklist
This checklist assumes familiarity with Airflow and its configuration. Note that enabling some of these options may
reduce or disable functionality needed for your particular use case. It is not a single solution for all
possible uses of Airflow and appropriate judgement must be used when applying these options.

There are two ways to set the settings for Airflow - via the ["airflow.cfg" file](https://github.com/apache/airflow/blob/master/airflow/config_templates/default_airflow.cfg) or by setting environment variables (AIRFLOW__{SECTION}\_\_{KEY}). Both options are presented below - see [docs](https://airflow.readthedocs.io/en/stable/howto/set-config.html).

# Table of Contents

- [Authentication Settings](#authentication-settings)
- [Authentication Settings for the API](#authentication-settings-for-the-api---see-docs)
- [Authorization Settings](#authorization-settings)
- [Disabling Dangerous Settings](#disabling-dangerous-settings)
- [Enabling Settings That Increase Security](#enabling-settings-that-increase-security)
- [SSL Settings](#ssl-settings)
- [Web UI Settings](#web-ui-settings)

## Authentication Settings
- [ ] **Enable authentication for email**
<details><summary>Using config file</summary>

  ```ini
  [smtp]
  smtp_user = <username>
  smtp_password = <password>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__SMTP__SMTP_USER=<username>
  AIRFLOW__SMTP__SMTP_PASSWORD=<password>
  ```
</details>

- [ ] **Enable authentication for Flower (BASIC only)**
<details><summary>Using config file</summary>

  ```ini
  [celery]
  flower_basic_auth = <user1>:<password1>,<user2>:<password2>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CELERY__FLOWER_BASIC_AUTH=<user1>:<password1>,<user2>:<password2>
  ```
</details>

- [ ] **Enable authentication for the scheduler**
<details><summary>Using config file</summary>

  ```ini
  [scheduler]
  authenticate = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__SCHEDULER__AUTHENTICATE=True
  ```
</details>

- [ ] **Turn on authentication for the web UI (username and password)**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  authenticate = True
  auth_backend = airflow.contrib.auth.backends.password_auth
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__AUTHENTICATE=True
  AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth
  ```
</details>

- [ ] **OR turn on authentication for the web UI (with a different backend - see [docs](https://airflow.readthedocs.io/en/stable/security.html#web-authentication))**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  authenticate = True
  auth_backend = <backend>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__AUTHENTICATE=True
  AIRFLOW__WEBSERVER__AUTH_BACKEND=<backend>
  ```
</details>

## Authentication Settings for the API - [see docs](https://airflow.apache.org/api.html)
- [ ] **Disable the REST API (which is exposed without authentication by default)**
<details><summary>Using config file</summary>

  ```ini
  [api]
  auth_backend = airflow.api.auth.backend.deny_all
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__API__AUTH_BACKEND=airflow.api.auth.backend.deny_all
  ```
</details>

- [ ] **OR turn on authentication (username and password)**
<details><summary>Using config file</summary>

  ```ini
  [api]
  auth_backend = airflow.contrib.auth.backends.password_auth
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__API__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth
  ```
</details>

- [ ] **OR turn on authentication (with a different backend - see [docs](https://airflow.readthedocs.io/en/stable/security.html#web-authentication)**
<details><summary>Using config file</summary>

  ```ini
  [api]
  auth_backend = <backend>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__API__AUTH_BACKEND=<backend>
  ```
</details>

## Authorization Settings
- [ ] **Enable web UI authorization**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  rbac = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__RBAC=True
  ```
</details>

- [ ] **Only show the user their own DAGs (requires authentication)**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  filter_by_owner = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__FILTER_BY_OWNER=True
  ```
</details>

## Disabling Dangerous Settings
- [ ] **Disable examples that ship with Airflow**
<details><summary>Using config file</summary>

  ```ini
  [core]
  load_examples = False
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__LOAD_EXAMPLES=False
  ```
</details>

- [ ] **Disable pickling (vulnerable to RCE)**
<details><summary>Using config file</summary>

  ```ini
  [core]
  donot_pickle = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__DONOT_PICKLE=True
  ```
</details>

- [ ] **Disable pickling of [XCom](https://airflow.apache.org/concepts.html?highlight=xcom#xcoms) between tasks (vulnerable to RCE)**
<details><summary>Using config file</summary>

  ```ini
  [core]
  enable_xcom_pickling = False
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__ENABLE_XCOM_PICKLING=False
  ```
</details>

- [ ] **Don't expose the configuration file via the web UI (if not using RBAC)**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  expose_config = False
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__EXPOSE_CONFIG=False
  ```
</details>

- [ ] **Prevent sudo for tasks that don't use impersonation by specifying the user to be used**
<details><summary>Using config file</summary>

  ```ini
  [core]
  default_impersonation = <user>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__DEFAULT_IMPERSONATION=<user>
  ```
</details>

## Enabling Settings That Increase Security
- [ ] **Change the Fernet key (you need to generate it then enable encryption via [these instructions](https://airflow.readthedocs.io/en/stable/howto/secure-connections.html))**
<details><summary>Using config file</summary>

  ```ini
  [core]
  fernet_key = <key>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__FERNET_KEY=<key>
  ```
</details>

- [ ] **Enable secure mode (turns off charts and ad-hoc queries)**
<details><summary>Using config file</summary>

  ```ini
  [core]
  secure_mode = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__SECURE_MODE=True
  ```
</details>

- [ ] **Restrict access to the web UI via network controls**

- [ ] **Turn on remote logging so logs are preserved if your system is
compromised (see [documentation](https://airflow.readthedocs.io/en/stable/howto/write-logs.html) )**

## SSL Settings
- [ ] **Enable SSL for Celery ([docs](https://airflow.readthedocs.io/en/stable/security.html#ssl))**
<details><summary>Using config file</summary>

  ```ini
  [celery]
  ssl_active = True
  ssl_key = <path to key>
  ssl_cert = <path to cert>
  ssl_cacert = <path to cacert>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CELERY__SSL_ACTIVE=True
  AIRFLOW__CELERY__SSL_KEY=<path to key>
  AIRFLOW__CELERY__SSL_CERT=<path to cert>
  AIRFLOW__CELERY__SSL_CACERT=<path to cacert>
  ```
</details>

- [ ] **Enable SSL for the Celery database connection (PostgreSQL, other engines need their own SSL flag set)**
<details><summary>Using config file</summary>

  ```ini
  [celery]
  result_backend = postgresql://<usr>:<pass>@<host>:<port>/<db>?sslmode=verify-full
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CELERY__RESULT_BACKEND=postgresql://<usr>:<pass>@<host>:<port>/<db>?sslmode=verify-full
  ```
</details>

- [ ] **Enable SSL for the metadata database connection (PostgreSQL, other engines need their own SSL flag set)**
<details><summary>Using config file</summary>

  ```ini
  [core]
  sql_alchemy_conn=postgresql://<usr>:<pass>@<host>:<port>/<db>?sslmode=verify-full
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://<usr>:<pass>@<host>:<port>/<db>?sslmode=verify-full
  ```
</details>

- [ ] **Enable SSL for DASK (if using)**
<details><summary>Using config file</summary>

  ```ini
  [dask]
  tls_key = <path to key>
  tls_cert = <path to cert>
  tls_ca = <path to cacert>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__DASK__TLS_KEY=<path to key>
  AIRFLOW__DASK__TLS_CERT=<path to cert>
  AIRFLOW__DASK__TLS_CACERT=<path to cacert>
  ```
</details>

- [ ] **Enable SSL for email**
<details><summary>Using config file</summary>

  ```ini
  [smtp]
  smtp_ssl = True
  smtp_starttls = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__SMTP__SMTP_SSL=True
  AIRFLOW__SMTP__STARTTLS=True
  ```
</details>

- [ ] **Enable SSL for LDAP - ldaps and port 636 (if using LDAP backends)**
<details><summary>Using config file</summary>

  ```ini
  [ldap]
  uri = ldaps://<host>:636
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__LDAP__URI=ldaps://<host>:636
  ```
</details>

- [ ] **Enable SSL for the web UI - if not using an SSL server in front of Airflow ([docs](https://airflow.readthedocs.io/en/stable/security.html#ssl))**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  web_server_ssl_cert = <path to cert>
  web_server_ssl_key = <path to key>
  web_server_port = 443
  base_url = https://<host>:443
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__WEB_SERVER_SSL_CERT=<path to cert>
  AIRFLOW__WEBSERVER__WEB_SERVER_SSL_KEY=<path to key>
  AIRFLOW__WEBSERVER__WEB_SERVER_PORT=443
  AIRFLOW__WEBSERVER__BASE_URL=https://<host>:443
  ```
</details>

## Web UI Settings
- [ ] **Change the [Flask secret key](https://flask.palletsprojects.com/en/1.0.x/config/#SECRET_KEY) to something random (you need to generate it)**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  secret_key = <key>
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__SECRET_KEY=<key>
  ```
</details>

- [ ] **Hide sensitive variables in the UI**
<details><summary>Using config file</summary>

  ```ini
  [admin]
  hide_sensitive_variable_fields = True
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__ADMIN__HIDE_SENSITIVE_VARIABLE_FIELDS=True
  ```
</details>

- [ ] **Make session cookies more secure (Secure and SameSite flags)**
<details><summary>Using config file</summary>

  ```ini
  [webserver]
  cookie_secure = True
  cookie_samesite = Strict
  ```
</details>
<details><summary>Using environment variables</summary>

  ```sh
  AIRFLOW__WEBSERVER__COOKIE_SECURE=True
  AIRFLOW__WEBSERVER__COOKIE_SAMESITE=Strict
  ```
</details>


# Other Information

## Related work:
   * [Airflow security documentation](https://airflow.apache.org/security.html)
   * [Airflow REST API authentication documentation](https://airflow.apache.org/api.html#authentication)
   * [Google Cloud list of blocked Airflow configurations](https://cloud.google.com/composer/docs/concepts/airflow-configurations)

## Reporting bugs and feature requests
Please use the GitHub issue tracker to report issues or suggest features:
https://github.com/nightwatchcybersecurity/airflowscan

You can also send emai to **research /at/ nightwatchcybersecurity [dot] com**
