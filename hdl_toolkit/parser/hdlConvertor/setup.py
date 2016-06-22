import os
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.sysconfig import customize_compiler

class buildWithoutStrictPrototypes(build_ext):
    def build_extensions(self):
        customize_compiler(self.compiler)
        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except (AttributeError, ValueError):
            pass
        build_ext.build_extensions(self)


BASE = "src/"
def collectFiles(baseDir ):
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            if (file.endswith(".c") or file.endswith(".cpp")) and not file.endswith("main.c"):
                yield os.path.join(root, file)

ALL_SOURCE = [] + list(collectFiles(BASE))



module1 = Extension('hdlConvertor',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include'],
                    library_dirs = ['/usr/local/lib'],
                    libraries = ['libantlr4-runtime'],
                    extra_compile_args=['-std=c++11'],
                    sources = ALL_SOURCE)

setup (cmdclass = {'build_ext': buildWithoutStrictPrototypes},
       name = 'hdlConvertor',
       author = 'aaaaaaaaaa',
       author_email = 'sadfas@sdfa.sa',
       ext_modules = [module1])
