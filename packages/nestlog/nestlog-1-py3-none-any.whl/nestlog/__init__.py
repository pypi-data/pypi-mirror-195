r"""
=======
NestLog
=======
Fancy tree logger for excellent shell output.  Uses :py:module:`click`
for shell colors.  Unlike the typical logger, the concept of "level" in
this logger refers to the depth of the tree.  So the higher the level,
the deeper the tree will display.

The nestlog logger has 3 status types:

.. list-table:: Statuses

    * - Status
      - Description
    * - okay
      - warn
      - fail
    * - `logger.okay('this is an okay message')`
    * - `logger.warn('this is an warn message')`
    * - `logger.fail('this is an fail message')`

.. image :: ../docs/images/level-3.png

Installation
============

..  code-block:: shell

    python -m pip install nestlog

Examples
========
Use the nestlog loggers `with` statement to control the depth of the log.

..  code-block:: python

    import nestlog

    logger = nestlog.NestLogger()

    with logger('starting application'):

        with logger('starting section 1'):
            logger.okay('doing something important')
            logger.okay('doing something else important')

        with logger('starting section 1'):
            logger.okay('doing something important')
            logger.okay('doing something else important')

"""
import datetime
import functools

import click

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
