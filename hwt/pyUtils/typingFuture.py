import inspect
import re
RE_CLASS_HEADER = re.compile(r'class.+\(([^,]*)(?:,\s*?(([^,]*)))*\)\s*\:')  # match comma separated IDs of base classes
ENABLE_CHECKING = False


def override(method):
    """
    Check that the method overrides the parent method. A temporal supplement for typing.override from python3.12

    Inspired by https://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method
    """
    if ENABLE_CHECKING:
        # stack()[0]=overrides, stack()[1]=inside class def'n, stack()[2]=outside class def'n
        stack = inspect.stack()[2]
        lineWithHeaderOfCurrentlyDefinedClass = stack[4][0]
        base_classes = RE_CLASS_HEADER.search(lineWithHeaderOfCurrentlyDefinedClass)
        if not base_classes:
            raise AssertionError("Can not detect base classes for checking if method overrides", lineWithHeaderOfCurrentlyDefinedClass)
        base_classes = base_classes.group(1)

        # handle multiple inheritance
        if not base_classes:
            raise ValueError('overrides decorator: unable to determine base class', lineWithHeaderOfCurrentlyDefinedClass)

        derived_class_locals = stack[0].f_locals

        for base_class in base_classes.split(','):
            base_class = base_class.strip()
            if '.' not in base_class:
                base_class = derived_class_locals[base_class]

            else:
                components = base_class.split('.')
                # obj is either a module or a class
                obj = derived_class_locals[components[0]]

                for c in components[1:]:
                    assert(inspect.ismodule(obj) or inspect.isclass(obj))
                    obj = getattr(obj, c)

                base_class = obj

            if hasattr(base_class, method.__name__):
                return method  # successfully found the method which is being overridden

        raise AssertionError(
            f"Does not override because any base class does not have this method ({method.__name__:s})")
    else:
        return method
