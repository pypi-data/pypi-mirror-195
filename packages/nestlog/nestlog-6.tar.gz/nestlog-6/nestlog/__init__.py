"""
==================
Welcome to NestLog
==================

|PyPiV| |Pipeline| |CodeCov| |QGStatus|

|Vuln| |Sec| |Bugs| |Rating| |Nlines|

|PyPiStatus| |PyPiVersion| |PyPiLicence|

Fancy tree logger for excellent shell output.  Uses the Click_ library
for shell colors.  Unlike the typical logger, the concept of "level" in
this logger refers to the depth of the tree.  So the higher the level,
the deeper the tree will display.

|Example|

============
Installation
============
nestlog is available on the public pypi.

..  code-block:: shell

    python -m pip install nestlog

========
Examples
========
Use the nestlog loggers `with` statement to control the depth of the log.

..  code-block:: python

    from nestlog import logger

    with logger('starting application'):

        with logger('starting section 1'):
            logger.okay('doing something important')
            logger.okay('doing something else important')

        with logger('starting section 1'):
            logger.okay('doing something important')
            logger.okay('doing something else important')

|Sonar|

|QualityGate|

.. |Example| image:: https://gitlab.com/sol-courtney/python-packages/nestlog/-/raw/2db9d610b7428400276f59d4feb06f84e15bfab2/docs/images/level-3.png
   :width: 400

.. |PyPiStatus| image:: https://img.shields.io/pypi/status/nestlog.svg
   :target: https://pypi.python.org/pypi/nestlog/

.. |PyPiVersion| image:: https://img.shields.io/pypi/pyversions/nestlog.svg
   :target: https://pypi.python.org/pypi/nestlog/

.. |PyPiV| image:: https://img.shields.io/pypi/v/nestlog.svg
   :target: https://pypi.python.org/pypi/nestlog/

.. |PyPiLicence| image:: https://img.shields.io/pypi/l/nestlog.svg
   :target: https://pypi.python.org/pypi/nestlog/

.. |CodeCov| image:: https://codecov.io/gl/sol-courtney:python-packages/nestlog/branch/develop/graph/badge.svg
   :target: https://codecov.io/gl/sol-courtney:python-packages/nestlog

.. |Pipeline| image:: https://gitlab.com/sol-courtney/python-packages/nestlog/badges/main/pipeline.svg
   :target: https://gitlab.com/sol-courtney/python-packages/nestlog

.. |Nlines| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=ncloc
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |Vuln| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=vulnerabilities
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |Sec| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=security_rating
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |Bugs| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=bugs
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |Rating| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=reliability_rating
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |Sonar| image:: https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |QualityGate| image:: https://sonarcloud.io/api/project_badges/quality_gate?project=sol-courtney_nestlog
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. |QGStatus| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_nestlog&metric=alert_status
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_nestlog

.. _Click: https://click.palletsprojects.com/

""" # noqa
__all__ = ('NestLogger', 'logger')

import datetime
import functools

import click

# --------------------------------------------------------------------------- #

SPACE: str = ' '
PIPE: str = '|'
INDENT: str = SPACE * 2 + PIPE
YBOX = click.style('warn', fg='yellow', bold=True)
GBOX = click.style('okay', fg='green', bold=True)
RBOX = click.style('fail', fg='red', bold=True)
STATUS_MAP = {0: GBOX, 1: YBOX, 2: RBOX}
ARROW = click.style('>>>', bold=True)
SUB_ARROW = '├──'
DONE_SLUG = click.style('done', fg='cyan', bold=True)
DONE = f'└──[{DONE_SLUG!s}]'

# --------------------------------------------------------------------------- #


class NestLogger:

    """Nestlog logger class.

    Use the `with` statement to control the depth of the tree.

    Parameters
    ----------
    verbose : int (optional)
        Set the depth that will be displayed.  By default, the entire
        tree is displayed, but if you want just the first 2 levels
        you can set this to `2`.

    Examples
    --------
    >>> import nestlog
    >>> logger = nestlog.NestLogger()
    >>> with logger('starting application'):
    ...     with logger('starting section 1'):
    ...         logger.okay('doing something important')
    ...         logger.warn('doing something else important')
    ...     with logger('starting section 1'):
    ...         logger.fail('doing something important')
    ...         logger.okay('doing something else important')

    """

    @property
    def now(self) -> datetime.datetime:
        return datetime.datetime.now()

    @property
    def active(self) -> bool:
        return (self.level <= self.verbose) or (self.verbose < 0)

    @property
    def indent(self) -> str:
        return (INDENT * self.level)

    def __init__(self, verbose: int = -1):
        """Nestlog logger class.

        Use the `with` statement to control the depth of the tree.

        Parameters
        ----------
        verbose : int (optional)
            Set the depth that will be displayed.  By default, the entire
            tree is displayed, but if you want just the first 2 levels
            you can set this to `2`.

        Examples
        --------
        >>> import nestlog
        >>> logger = nestlog.NestLogger()
        >>> with logger('starting application'):
        ...     with logger('starting section 1'):
        ...         logger.okay('doing something important')
        ...         logger.warn('doing something else important')
        ...     with logger('starting section 1'):
        ...         logger.fail('doing something important')
        ...         logger.okay('doing something else important')

        """
        self.verbose: int = verbose if (verbose >= 0) else 1000
        self.level: int = 0
        self._last: str = ''

    def __call__(self, message: str = None):
        if message and self.active:
            msg = click.style(message, fg='cyan', bold=True)
            if (self.verbose >= 2) and (self.level < self.verbose): # noqa
                click.echo(self.indent)
            if self.level:
                arrow = SUB_ARROW
                if self.level < self.verbose:
                    line = '───'
                else:
                    line = ''
                msg = f'{line!s}[{msg!s}]'
            else:
                arrow = ARROW
                msg = f' {msg!s}'
            click.echo(f'{self.indent[:-1]!s}{arrow}{msg!s}')
            self._last = 'section'
        return self

    def __enter__(self):
        self._t0 = self.now
        self.level += 1
        return self

    def __exit__(self, *exc):
        if self.active:
            msg = f'{self.indent[:-1]!s}{DONE!s}'
            td = (self.now - self._t0).total_seconds()
            msg += f' {td!s}'
            if self._last == 'close':
                click.echo(self.indent)
            click.echo(msg)
            self._last = 'close'
        self.level -= 1
        return False

    def emit(self, message: str, status: int = 0):
        if self.active:
            status = STATUS_MAP.get(status, RBOX)
            box = f'├──[{status!s}]'
            click.echo(f'{self.indent[:-1]!s}{box!s} {message!s}')
            self._last = 'emit'

    okay = functools.partialmethod(emit, status=0)
    warn = functools.partialmethod(emit, status=1)
    fail = functools.partialmethod(emit, status=2)


logger = NestLogger()
