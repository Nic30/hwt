from distutils.core import setup, Extension
import os

ANTLR = 'antlr4-runtime-cpp/'

ANTRL_INCLUDE = [
                 ANTLR,
                 ANTLR+"/misc",
                 ANTLR+"/atn",
                 ANTLR+"/dfa",
                 ANTLR+"/tree",
                 ANTLR+"/support",
                ]  
BASE = "src/"
ALL_SOURCE = []

def collectFiles(baseDir ):
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            if (file.endswith(".c") or file.endswith(".cpp")) and not file.endswith("main.c"):
                yield os.path.join(root, file)

ALL_SOURCE += list(collectFiles(BASE))
for d in ANTRL_INCLUDE:
    ALL_SOURCE += list(collectFiles(d))



module1 = Extension('hdlConvertor',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include']  + ANTRL_INCLUDE,
                    library_dirs = ['/usr/local/lib'],
                    extra_compile_args=['-std=c++11'],
                    sources = ALL_SOURCE)

setup (name = 'hdlConvertor',
       author = 'aaaaaaaaaa',
       author_email = 'sadfas@sdfa.sa',
       ext_modules = [module1])
