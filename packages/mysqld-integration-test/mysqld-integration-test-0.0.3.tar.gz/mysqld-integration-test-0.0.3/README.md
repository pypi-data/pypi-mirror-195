# mysqld-integration-test
![](https://img.shields.io/pypi/v/mysqld-integration-test.svg) ![](https://img.shields.io/badge/status-alpha-red) ![](https://github.com/jasondcamp/mysqld-integration-test/actions/workflows/mysqld-integration-test.yml/badge.svg)  ![](https://img.shields.io/pypi/pyversions/mysqld-integration-test.svg)

![](https://api.codeclimate.com/v1/badges/e5505727f2fa988debcb/maintainability) ![](https://api.codeclimate.com/v1/badges/e5505727f2fa988debcb/test_coverage)

## Overview
mysqld-integration-test is a python module that creates a temporary mysqld instance to use for testing your application. It is based on the `testing.mysqld` module which has not been updated recently.

## Download and Install
To install use pip:

    $ pip install mysqld-integration-test

Or clone the repo:

    $ git clone https://github.com/jasondcamp/mysqld-integration-test.git

## Configuration
#### mysqld-integration-test environment variables and command line options

## Usage

#### import

```
from mysqld_integration_test import Mysqld
```

#### run
Starts up the mysql server

```
mysqld = Mysqld()
instance = mysqld.run()
```

#### stop
Stops the mysql server
```
mysqld.stop()
```

### Example

```
#!/usr/bin/env python3

from mysqld_integration_test import Mysqld
import mysql.connector

mysqld = Mysqld()
instance = mysqld.run()



mysqld.stop()
```



