# Prerequisite

The following should be installed already before setup.

- Python3
- npm
- MySql

# Getting Started

Install Required Libraries
```
python3 -m venv pymyenv
. pymyenv/bin/activate
make install
pip install flask-monitoringdashboard
```

Set Env Variables

```
python3 -c 'import secrets; print(secrets.token_urlsafe())'
export SECRET_KEY="YourSecrets"
python3 -c 'import secrets; print(secrets.SystemRandom().getrandbits(128))'
export SECURITY_PASSWORD_SALT="YourSalt"
export DATABASE_USER="YourDatabaseUserName"
export DATABASE_PASSWORD="YourDatabasePassword"
export DATABASE_HOST="YourDatabaseHost"
export DATABASE_NAME="YourDatabaseName"
export DATABASE_NAME_TEST="YourDatabaseName"
```

# How to run API

Run with the following command.
`dev`, `test`, are `prod` are supported to specify the enviroment.

```
python3 app.py dev
```

# API Doc

API Doc is built with OpenAPI and `redoc-cli`

```
npm install -g redoc-cli
```

If you want to make API document, run the following code.

```
make document
```

The exported document is published at [ssd_6/static/documents/api-document](https://shotakameyama.github.io/ssd_u6/static/documents/api-document)

# How to Run the test

Pytest/PyLint/Flake8/Bandit are used for the test.

```
make test
make lint
make flake8
make bandit
```

The exported documtnes are published below:

- PyTest result at [ssd_6/static/reports/pytest_report](https://shotakameyama.github.io/ssd_u6/static/reports/pytest_report)
- Flake8 result at [ssd_6/static/reports/flake8_report](https://shotakameyama.github.io/ssd_u6/static/reports/flake8_report)
- Bandit result at [ssd_6/static/reports/bandit_report](https://shotakameyama.github.io/ssd_u6/static/reports/bandit_report)


# How to run the automated security testing with OWASP ZAP

As the APIs are defined in the OpenAPI file, OWASP ZAP will provide the automated testing using it.

The exported document is publised below:
- OWASP ZAP test result at [ssd_u6/static/reports/owasp_zap_report](https://shotakameyama.github.io/ssd_u6/static/reports/owasp_zap_report)

For more details, please read [the official documents](https://www.zaproxy.org/docs/desktop/addons/openapi-support/).

# How to contribute

To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and check with: `make check`
4. Commit them: `git commit -m '<commit_message>'`
5. Push to the original branch: `git push origin ShotaKameyama/ssd_u6`
6. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
