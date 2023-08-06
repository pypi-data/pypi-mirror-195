# mysqld-integration-test

![](https://img.shields.io/badge/status-alpha-yellow)

version 0.0.2

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
mysqld.run()
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

mysqld = Mysqld()
mysqld.run()



mysqld.stop()
```



