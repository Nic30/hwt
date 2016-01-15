from setuptools import setup, find_packages

setup(name='HWToolkit',
      version='0.1',
      description='hdl synthesis toolkit',
      url='https://github.com/Nic30/HWToolkit',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      install_requires=[
        'slimit',
        'sympy',
        'jinja2', # vhdl templates renderer, visualizer renderer
        'ply',    # old parser, vhdl interpret
        'flask',  # visualizer
        'antlr4-python3-runtime', # vhdl parser, lexer
        "dill",   # for creating cache files
      ],
      license='MIT',
      packages = find_packages(),
      #packages=['hls_toolkit', 'cpp_toolkit', 'python_toolkit', 'tcl_toolkit',\
      #          'vivado_toolkit', 'vhdl_toolkit' ],
      zip_safe=False)
