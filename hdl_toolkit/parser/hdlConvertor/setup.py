from distutils.core import setup, Extension

module1 = Extension('hdlConvertor',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include'],
                    library_dirs = ['/usr/local/lib'],
                    sources = ['src/hdlConvertorModule.cpp'])

setup (name = 'hdlConvertor',
       author = 'aaaaaaaaaa',
       author_email = 'sadfas@sdfa.sa',
       ext_modules = [module1])