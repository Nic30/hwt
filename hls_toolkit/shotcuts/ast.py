import  ast

import hls_toolkit.errors as errors
import myhdl


def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, level)) for a, b in ast.iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)
    
    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

def Call_simple(fn_id, args=[]):
    return ast.Call(func=ast.Name(id=fn_id), args=args, keywords=(), kwargs=(), starargs=None)

def addSignal(fnNode, name, sigType):
    indx = 0
    # skip docstring
    for i in fnNode.body:
        if isinstance(i, ast.Expr) and isinstance(i.value, ast.Str):
            indx += 1
        else:
            break
    if isinstance(sigType, bool) or sigType == bool:
        sigType = [Call_simple("bool", [])]
    elif isinstance(sigType, myhdl.intbv):
        sigType = [ast.Subscript(
                                 value=Call_simple("intbv", [ast.Num(sigType._val)]),
                                 slice=ast.Slice(lower=ast.Num(sigType._nrbits), upper=None, step=None))]
    else:
        raise NotImplementedError()
    fnNode.body.insert(indx, ast.Assign(targets=[ast.Name(id=name)],
                                        value=Call_simple("Signal", sigType)))
    
    
def fnFileAst(compFn):
    with open(compFn.__code__.co_filename) as f:
        tree = ast.parse(f.read())
    return tree

def nodeOfFn(tree, compFn):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and compFn.__code__.co_name == node.name:
            return node
