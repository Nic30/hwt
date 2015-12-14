# -*- coding: utf-8 -*-
"""
purpose is to fake exception origin and virtualy throw it from template file like jinja2 and other does
"""

import ctypes
import sys
from types import TracebackType, CodeType


iteritems = lambda d: iter(d.items())

# raise helper hack
raise_helper = 'raise __hls_exception__[1]'

def translate_syntax_error(error, source=None):
    """Rewrites a syntax error to please traceback systems."""
    error.source = source
    error.translated = True
    exc_info = (error.__class__, error, None)
    filename = error.filename
    if filename is None:
        filename = '<unknown>'
    return fake_exc_info(exc_info, filename, error.lineno)

def _init_tb_set_next():
    """This function implements a few ugly things so that we can patch the
    traceback objects.  The function returned allows resetting `tb_next` on
    any python traceback object.  Do not attempt to use this on non cpython
    interpreters
    """

    # figure out size of _Py_ssize_t
    if hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
        _Py_ssize_t = ctypes.c_int64
    else:
        _Py_ssize_t = ctypes.c_int

    # regular python
    class _PyObject(ctypes.Structure):
        pass
    _PyObject._fields_ = [
        ('ob_refcnt', _Py_ssize_t),
        ('ob_type', ctypes.POINTER(_PyObject))
    ]

    # python with trace
    if hasattr(sys, 'getobjects'):
        class _PyObject(ctypes.Structure):
            pass
        _PyObject._fields_ = [
            ('_ob_next', ctypes.POINTER(_PyObject)),
            ('_ob_prev', ctypes.POINTER(_PyObject)),
            ('ob_refcnt', _Py_ssize_t),
            ('ob_type', ctypes.POINTER(_PyObject))
        ]

    class _Traceback(_PyObject):
        pass
    _Traceback._fields_ = [
        ('tb_next', ctypes.POINTER(_Traceback)),
        ('tb_frame', ctypes.POINTER(_PyObject)),
        ('tb_lasti', ctypes.c_int),
        ('tb_lineno', ctypes.c_int)
    ]

    def tb_set_next(tb, nextFrm):
        """Set the tb_next attribute of a traceback object."""
        if not (isinstance(tb, TracebackType) and
                (nextFrm is None or isinstance(nextFrm, TracebackType))):
            raise TypeError('tb_set_next arguments must be traceback objects')
        obj = _Traceback.from_address(id(tb))
        if tb.tb_next is not None:
            old = _Traceback.from_address(id(tb.tb_next))
            old.ob_refcnt -= 1
        if nextFrm is None:
            obj.tb_next = ctypes.POINTER(_Traceback)()
        else:
            nextFrm = _Traceback.from_address(id(nextFrm))
            nextFrm.ob_refcnt += 1
            obj.tb_next = ctypes.pointer(nextFrm)

    return tb_set_next

def fake_exc_info(exc_info, filename, lineno):
    """Helper for `translate_exception`."""
    exc_type, exc_value, tb = exc_info

    # figure the real context out
    if tb is not None:
        real_locals = tb.tb_frame.f_locals.copy()
        ctx = real_locals.get('context')
        if ctx:
            locals = ctx.get_all()
        else:
            locals = {}
        for name, value in iteritems(real_locals):
            if name.startswith('l_') and value is not missing:
                locals[name[2:]] = value

        # if there is a local called __hls_exception__, we get
        # rid of it to not break the debug functionality.
        locals.pop('__hls_exception__', None)
    else:
        locals = {}

    # assamble fake globals we need
    globals = {
        '__name__':             filename,
        '__file__':             filename,
        '__hls_exception__':  exc_info[:2],

        # we don't want to keep the reference to the template around
        # to not cause circular dependencies, but we mark it as hls
        # frame for the ProcessedTraceback
        '__hls_template__':   None
    }

    # and fake the exception
    code = compile('\n' * (lineno - 1) + raise_helper, filename, 'exec')

    # if it's possible, change the name of the code.  This won't work
    # on some python environments such as google appengine
    try:
        if tb is None:
            location = 'template'
        else:
            function = tb.tb_frame.f_code.co_name
            if function == 'root':
                location = 'top-level template code'
            elif function.startswith('block_'):
                location = 'block "%s"' % function[6:]
            else:
                location = 'template'
        code = CodeType(0, code.co_nlocals, code.co_stacksize,
                        code.co_flags, code.co_code, code.co_consts,
                        code.co_names, code.co_varnames, filename,
                        location, code.co_firstlineno,
                        code.co_lnotab, (), ())
    except:
        pass

    # execute the code and catch the new traceback
    try:
        exec(code, globals, locals)
    except:
        exc_info = sys.exc_info()
        new_tb = exc_info[2].tb_next

    # return without this frame
    return exc_info[:2] + (new_tb,)

tb_set_next = _init_tb_set_next()

#
#if __name__ == "__main__":
#    HLSTeplateErr._raise("wrong syntax", "/home/nic30/Documents/workspace/hw_synthesis/hw_synthesis_helpers/hls_toolkit/debug.py", 99999)


