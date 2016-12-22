# byteplay: CPython assembler/disassembler
# Copyright (C) 2006 Noam Raphael | Version: http://code.google.com/p/byteplay
# Rewritten 2009 Demur Rumed | Version: http://github.com/serprex/byteplay
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
__version__ = '0.2'

from dis import findlabels
import opcode

from hwt.pyUtils.optCodes import _se, _rf, Opcode, hascode, LOAD_CONST, hasarg, \
     hasconst, hasname, hasjabs, hasflow, hasjump, haslocal, hascompare, \
     hasfree, hasjrel, cmp_op, SETUP_FINALLY, BREAK_LOOP, RETURN_VALUE, RAISE_VARARGS, \
    FOR_ITER, JUMP_FORWARD, JUMP_ABSOLUTE, JUMP_IF_FALSE_OR_POP, \
    JUMP_IF_TRUE_OR_POP, CONTINUE_LOOP, SETUP_LOOP, SETUP_EXCEPT, POP_BLOCK, \
    END_FINALLY, WITH_CLEANUP, STORE_NAME, LOAD_NAME, DELETE_NAME, YIELD_VALUE, \
    LOAD_GLOBAL, LOAD_FAST, CALL_FUNCTION, POP_TOP
from types import CodeType
import dis

def getse(op, arg=None):
    if op in _se:return _se[op]
    if arg is None:raise ValueError("%s requires arg" % op)
    if op in _rf:return _rf[op](arg)
    raise ValueError("Unknown %s %s" % (op, arg))

class Label(object):
    pass

class SetLinenoType(object):
    def __repr__(self):
        return 'SetLineno'
SetLineno = SetLinenoType()


def isopcode(x):
    return x is not SetLineno and not isinstance(x, Label)

CO_OPTIMIZED = 1
CO_NEWLOCALS = 2
CO_VARARGS = 4
CO_VARKEYWORDS = 8
CO_NESTED = 16
CO_GENERATOR = 32
CO_NOFREE = 64
CO_GENERATOR_ALLOWED = 0x1000
CO_FUTURE_DIVISION = 0x2000
CO_FUTURE_ABSOLUTE_IMPORT = 0x4000
CO_FUTURE_WITH_STATEMENT = 0x8000

class Code(object):
    """An object which holds all the information which a Python code object
    holds, but in an easy-to-play-with representation

    The attributes are:

    Affecting action
    code - list of 2-tuples: the code
    freevars - list of strings: the free vars of the code (those are names
               of variables created in outer functions and used in the function)
    args - list of strings: the arguments of the code
    varargs - boolean: Does args end with a '*args' argument
    varkwargs - boolean: Does args end with a '**kwargs' argument
    newlocals - boolean: Should a new local namespace be created.
                (True in functions, False for module and exec code)

    Not affecting action
    name - string: the name of the code (co_name)
    filename - string: the file name of the code (co_filename)
    firstlineno - int: the first line number (co_firstlineno)
    docstring - string or None: the docstring (the first item of co_consts,
                if it's str or unicode)

    code is a list of 2-tuples. The first item is an opcode, or SetLineno, or a
    Label instance. The second item is the argument, if applicable, or None"""
    def __init__(self, code, freevars, args, varargs, \
                  varkwargs, newlocals, name, filename, firstlineno, docstring):
        self.code = code
        self.freevars = freevars
        self.args = args
        self.varargs = varargs
        self.varkwargs = varkwargs
        self.newlocals = newlocals
        self.name = name
        self.filename = filename
        self.firstlineno = firstlineno
        self.docstring = docstring
        
    @staticmethod
    def _findlinestarts(code):
        """Find the offsets in a byte code which are start of lines in the source
        Generate pairs offset,lineno as described in Python/compile.c
        This is a modified version of dis.findlinestarts, which allows multiplelinestarts with the same line number"""
        lineno = code.co_firstlineno
        addr = 0
        for byte_incr, line_incr in zip(code.co_lnotab[0::2], code.co_lnotab[1::2]):
            if byte_incr:
                yield addr, lineno
                addr += byte_incr
            lineno += line_incr
        yield addr, lineno
        
    @classmethod
    def from_code(cls, co):
        """Disassemble a Python code object into a Code object"""
        co_code = co.co_code
        labels = dict((addr, Label()) for addr in findlabels(co_code))
        linestarts = dict(cls._findlinestarts(co))
        cellfree = co.co_cellvars + co.co_freevars
        code = []
        n = len(co_code)
        i = extended_arg = 0
        while i < n:
            op = Opcode(co_code[i])
            if i in labels:
                code.append((labels[i], None))
            if i in linestarts:
                code.append((SetLineno, linestarts[i]))
            i += 1
            if op in hascode:
                lastop, lastarg = code[-1]
                if lastop != LOAD_CONST:
                    raise ValueError("%s should be preceded by LOAD_CONST code" % op)
                code[-1] = (LOAD_CONST, Code.from_code(lastarg))
            if op not in hasarg:
                code.append((op, None))
            else:
                arg = co_code[i] | co_code[i + 1] << 8 | extended_arg
                extended_arg = 0
                i += 2
                if op == opcode.EXTENDED_ARG:extended_arg = arg << 16
                else:
                    code.append((op, co.co_consts[arg] if op in hasconst else co.co_names[arg] if op in hasname else labels[arg] if op in hasjabs else labels[i + arg] if op in hasjrel else co.co_varnames[arg] if op in haslocal else cmp_op[arg] if op in hascompare else cellfree[arg] if op in hasfree else arg))
        varargs = not not co.co_flags & CO_VARARGS
        varkwargs = not not co.co_flags & CO_VARKEYWORDS
        return cls(code=code,
                freevars=co.co_freevars,
                args=co.co_varnames[:co.co_argcount + varargs + varkwargs],
                varargs=varargs,
                varkwargs=varkwargs,
                newlocals=not not co.co_flags & CO_NEWLOCALS,
                name=co.co_name,
                filename=co.co_filename,
                firstlineno=co.co_firstlineno,
                docstring=co.co_consts[0] if co.co_consts and isinstance(co.co_consts[0], str) else None)
        
    def __eq__(self, other):
        try:
            if(self.freevars != other.freevars or
            self.args != other.args or
            self.varargs != other.varargs or
            self.varkwargs != other.varkwargs or
            self.newlocals != other.newlocals or
            self.name != other.name or
            self.filename != other.filename or
            self.firstlineno != other.firstlineno or
            self.docstring != other.docstring or
            len(self.code) != len(other.code)):return False
            # This isn't trivial due to labels
            lmap = {}
            for (op1, arg1), (op2, arg2) in zip(self.code, other.code):
                if isinstance(op1, Label):
                    if lmap.setdefault(arg1, arg2) is not arg2:return False
                else:
                    if op1 != op2:return False
                    if op1 in hasjump:
                        if lmap.setdefault(arg1, arg2) is not arg2:return False
                    elif arg1 != arg2:return False
            return True
        except:
            return False
        
    def _compute_stacksize(self):
        code = self.code
        label_pos = dict((op[0], pos) for pos, op in enumerate(code) if isinstance(op[0], Label))
        # sf_targets are the targets of SETUP_FINALLY opcodes. They are recorded
        # because they have special stack behaviour. If an exception was raised
        # in the block pushed by a SETUP_FINALLY opcode, the block is popped
        # and 3 objects are pushed. On return or continue, the block is popped
        # and 2 objects are pushed. If nothing happened, the block is popped by
        # a POP_BLOCK opcode and 1 object is pushed by a (LOAD_CONST, None)
        # operation
        # Our solution is to record the stack state of SETUP_FINALLY targets
        # as having 3 objects pushed, which is the maximum. However, to make
        # stack recording consistent, the get_next_stacks function will always
        # yield the stack state of the target as if 1 object was pushed, but
        # this will be corrected in the actual stack recording
        sf_targets = set(label_pos[arg] for op, arg in code if op == SETUP_FINALLY)
        stacks = [None] * len(code)
        maxsize = 0
        op = [(0, (0,))]
        def newstack(n):
            if curstack[-1] < -n:raise ValueError("Popped a non-existing element at %s %s" % (pos, code[pos - 3:pos + 2]))
            return curstack[:-1] + (curstack[-1] + n,)
        while op:
            pos, curstack = op.pop()
            o = sum(curstack)
            if o > maxsize:maxsize = o
            o, arg = code[pos]
            if isinstance(o, Label):
                if pos in sf_targets:curstack = curstack[:-1] + (curstack[-1] + 2,)
                if stacks[pos] is None:
                    stacks[pos] = curstack
                    if o not in (BREAK_LOOP, RETURN_VALUE, RAISE_VARARGS):
                        pos += 1
                        if not isopcode(o):
                            op += (pos, curstack),
                        elif o not in hasflow:
                            op += (pos, newstack(getse(o, arg))),
                        elif o == FOR_ITER:
                            op += (label_pos[arg], newstack(-1)), (pos, newstack(1))
                        elif o in (JUMP_FORWARD, JUMP_ABSOLUTE):
                            op += (label_pos[arg], curstack),
                        elif o in (JUMP_IF_FALSE_OR_POP, JUMP_IF_TRUE_OR_POP):
                            op += (label_pos[arg], curstack), (pos, curstack)
                        elif o == CONTINUE_LOOP:
                            op += (label_pos[arg], curstack[:-1]),
                        elif o == SETUP_LOOP:
                            op += (pos, curstack + (0,)), (label_pos[arg], curstack)
                        elif o == SETUP_EXCEPT:
                            op += (pos, curstack + (0,)), (label_pos[arg], newstack(3))
                        elif o == SETUP_FINALLY:
                            op += (pos, curstack + (0,)), (label_pos[arg], newstack(1))
                        elif o == POP_BLOCK:
                            op += (pos, curstack[:-1]),
                        elif o == END_FINALLY:
                            op += (pos, newstack(-3)),
                        elif o == WITH_CLEANUP:
                            op += (pos, newstack(-1)),
                        else:raise ValueError("Unhandled opcode %s" % op)
                elif stacks[pos] != curstack:
                    o = pos + 1
                    while code[o][0] not in hasflow:o += 1
                    if code[o][0] not in (RETURN_VALUE, RAISE_VARARGS):
                        raise ValueError("Inconsistent code at %s %s %s\n%s" % (pos, curstack, stacks[pos], code[pos - 5:pos + 4]))
        return maxsize
    
    def to_code(self):
        """Assemble a Python code object from a Code object"""
        co_argcount = len(self.args) - self.varargs - self.varkwargs
        co_stacksize = self._compute_stacksize()
        co_flags = set(op[0] for op in self.code)
        co_flags = (not(STORE_NAME in co_flags or LOAD_NAME in co_flags or DELETE_NAME in co_flags))  \
                    | (self.newlocals and CO_NEWLOCALS)                                               \
                    | (self.varargs and CO_VARARGS)                                                   \
                    | (self.varkwargs and CO_VARKEYWORDS)                                             \
                    | ((YIELD_VALUE in co_flags) << 5) | ((not co_flags & hasfree) << 6)
        co_consts = [self.docstring]
        co_names = []
        co_varnames = list(self.args)
        co_freevars = tuple(self.freevars)
        # Find all cellvars beforehand for two reasons
        # Need the number of them to construct the numeric arg for ops in hasfree
        # Need to put args which are cells in the beginning of co_cellvars
        cellvars = set(arg for op, arg in self.code
                if isopcode(op) and op in hasfree
                and arg not in co_freevars)
        co_cellvars = [jumps for jumps in self.args if jumps in cellvars]

        def index(seq, item, eq=True, can_append=True):
            for i, x in enumerate(seq):
                if x == item if eq else x is item:return i
            if can_append:
                seq.append(item)
                return len(seq) - 1
            else:
                raise IndexError("Item not found")

        jumps = []
        label_pos = {}
        lastlineno = self.firstlineno
        lastlinepos = 0
        co_code = bytearray()
        co_lnotab = bytearray()
        for i, (op, arg) in enumerate(self.code):
            if isinstance(op, Label):
                label_pos[op] = len(co_code)
            elif op is SetLineno:
                incr_lineno = arg - lastlineno
                incr_pos = len(co_code) - lastlinepos
                lastlineno = arg
                lastlinepos += incr_pos
                if not (incr_lineno or incr_pos):co_lnotab += b"\0\0"
                else:
                    while incr_pos > 255:
                        co_lnotab += b"\xFF\0"
                        incr_pos -= 255
                    while incr_lineno > 255:
                        co_lnotab += b"%c\xFF" % incr_pos
                        incr_pos = 0
                        incr_lineno -= 255
                    if incr_pos or incr_lineno:
                        co_lnotab += ("%c%c" % (incr_pos, incr_lineno)).encode()
            elif op == opcode.EXTENDED_ARG:
                self.code[i + 1][1] |= 1 << 32
            elif op not in hasarg:
                co_code += ("%c" % op).encode()
            else:
                if op in hasconst:
                    if isinstance(arg, Code) and i + 1 < len(self.code) and self.code[i + 1][0] in hascode:
                        arg = arg.to_code()
                    arg = index(co_consts, arg, 0)
                elif op in hasname:
                    arg = index(co_names, arg)
                elif op in hasjump:
                    jumps.append((len(co_code), arg))
                    arg = None
                elif op in haslocal:
                    arg = index(co_varnames, arg)
                elif op in hascompare:
                    arg = index(cmp_op, arg, can_append=False)
                elif op in hasfree:
                    try:
                        arg = index(co_freevars, arg, can_append=False) + len(cellvars)
                    except IndexError:
                        arg = index(co_cellvars, arg)
                if arg is not None and arg > 0xFFFF:
                    co_code += ("%c%c%c" % (opcode.EXTENDED_ARG, arg >> 16 & 0xFF, arg >> 24 & 0xFF)).encode()
                co_code += ("%c\0\0" % op if arg is None else "%c%c%c" % (op, arg & 0xFF, arg >> 8 & 0xFF)).encode()
        for pos, label in jumps:
            jump = label_pos[label]
            if co_code[pos] in hasjrel:
                jump -= pos + 3
            if jump > 0xFFFF:
                raise NotImplementedError("Extended jumps not implemented")
            co_code[pos + 1] = jump & 0xFF
            co_code[pos + 2] = jump >> 8
            
            
        if not self.varkwargs:
            kwonlyargcount = 0
        else:
            raise NotImplementedError()
            
        return CodeType(co_argcount, kwonlyargcount, len(co_varnames),
                        co_stacksize, co_flags, bytes(co_code),
                        tuple(co_consts), tuple(co_names), tuple(co_varnames),
                         self.filename, self.name, self.firstlineno,
                         bytes(co_lnotab), co_freevars, tuple(co_cellvars))
    
    def insertInCode(self, stratIndex, instructions):
        for i in instructions:
            c.code.insert(stratIndex, i)
            stratIndex += 1
            
    
    def addPositionalArg(self, argName):
        self.args = (argName,) + self.args

if __name__ == "__main__":
    def fn(a, a_en, b):
        print('With synthesizer')
        if a_en:
            return a
    
        
    c = Code.from_code(fn.__code__)
    argName = "__synthesizer__"
    c.addPositionalArg(argName)
    
    
    
    for i in c.code:
        print(i)
    
    #instr = [
    #    (Opcode(LOAD_GLOBAL), 'print'),
    #    (Opcode(LOAD_CONST), 'With synthesizer'),
    #    #(Opcode(LOAD_FAST), '__synthesizer__')  ,
    #    (Opcode(CALL_FUNCTION), 1),
    #    (Opcode(POP_TOP), None),
    #]
    #c.insertInCode(1, instr)
    print()
    for i in c.code:
        print(i)
    
    dis.dis(fn.__code__)
    
    fn.__code__ = c.to_code()
    print("\n\n")
    dis.dis(fn.__code__)
    print(fn(True, 10, True, 20))
    
    
