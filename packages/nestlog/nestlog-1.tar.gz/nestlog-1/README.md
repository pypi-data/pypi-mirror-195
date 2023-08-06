[![PyPi Latest](https://img.shields.io/pypi/v/nestlog.svg)](https://pypi.org/project/nestlog/)
[![Build](https://gitlab.com/sol-courtney/python-packages/nestlog/badges/main/pipeline.svg)](https://gitlab.com/sol-courtney/python-packages/nestlog)
[![Codecov](https://codecov.io/gl/sol-courtney:python-packages/nestlog/branch/develop/graph/badge.svg)](https://codecov.io/gl/sol-courtney:python-packages/nestlog)
[![Docs](https://readthedocs.org/projects/nestlog/badge/?version=latest)](https://nestlog.readthedocs.io)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)

[![Package Status](https://img.shields.io/pypi/status/nestlog.svg)](https://pypi.org/project/nestlog/)
[![PyVersions](https://img.shields.io/pypi/pyversions/nestlog.svg)](https://pypi.org/project/nestlog/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/nestlog.svg?label=PyPI%20downloads)](https://pypi.org/project/nestlog/)

[![License](https://img.shields.io/pypi/l/nestlog.svg)](https://gitlab.com/sol-courtney/python-packages/nestlog/-/blob/main/LICENSE)

# Welcome to Nestlog
nestlog is a formatted shell logger for producing colored tree like logs.

See the [Documentation](https://nestlog.readthedocs.io) for more help.

## Installation

From [PyPI](https://pypi.org/project/nestlog/) directly:

```
pip install nestlog
```

## Examples
This is how you use the logger

```py
import nestlog

logger = nestlog.NestLogger()

with logger('starting application'):

    with logger('starting section 1'):
        logger.okay('doing something important')
        logger.warn('warning message')
        logger.fail('failure message')

    with logger('starting section 1'):
        logger.okay('doing something important')
        logger.okay('doing something else important')
```

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)

[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=sol-courtney_nestlog)](https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog)
