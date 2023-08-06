import os as _os

import neaty
import neaty.neaty


def _envbool(name, default):
    """
    Read boolean from environment variable *name* or from *default*.

    Expect environment variable to be 'true' or 'false', return
    respective boolean.  Raise ValueError if the value is different.
    If the variable is unset, use *default* as default value.
    """
    value = _os.environ.get(name, default)
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise ValueError("invalid value: %s=%s" % (name, value))


_logger = neaty.make_logger(
    debug=_envbool('NEATY_DEBUG', 'false'),
    verbose=_envbool('NEATY_VERBOSE', 'false'),
    ltype=_os.environ.get('NEATY', 'plain'),
)


class Debuggable:
    """
    Pretty's favorite base object

    Makes some debug logging related activities easier.  Sub-classed
    objects inherit  __repr__() that uses _dscalar and _dlist class
    attributes to describe the instance.  _dscalar and _dlist are
    lists of names of attributes that can be made part of the
    description; attributes in _dscalar will be described using
    repr(), for attributes in _dlist will only length is shown as
    description.  (This is useful for attributes that can have long
    lists.)

    _log_birth() is another utility function that is best called
    last item in __init__() method and will try to describe the
    newborn instance.
    """

    _dscalar: list[str] = []
    _dlist: list[str] = []
    _logger: neaty.neaty.Logger = _logger

    def __repr__(self):
        cn = self.__class__.__name__
        ss = ['%s=%r' % (a, getattr(self, a))
              for a in self._dscalar]
        ls = ['len(%s)=%d' % (a, len(getattr(self, a)))
              for a in self._dlist]
        ss = ','.join(ss + ls)
        return '%s(%s)' % (cn, ss)

    def _log_birth(self):
        self._logger.debug('new %r' % self)

    def _log_state(self, mn, vn, vv):
        cn = self.__class__.__name__
        self._logger.debug('%s.%s():%s=%r' % (cn, mn, vn, vv))

    def _log_msg(self, mn, msg):
        cn = self.__class__.__name__
        self._logger.debug('%s.%s():%s' % (cn, mn, msg))


debug = _logger.debug
debugv = _logger.debugv
die = _logger.die
update_mode = _logger.update_mode
ltype = _logger.ltype
mode = _logger.mode
mkusage = _logger.mkusage
think = _logger.think
thinkv = _logger.thinkv
warn = _logger.warn
warnv = _logger.warnv


__all__ = [
    'Debuggable',
    'debug',
    'debugv',
    'die',
    'mkusage',
    'mode',
    'think',
    'thinkv',
    'warn',
    'warnv',
]
