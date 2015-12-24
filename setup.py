from setuptools import setup

setup(name='HWToolkit',
      version='0.1',
      description='hdl synthesis toolkit',
      url='https://github.com/Nic30/HWToolkit',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      license='MIT',
      packages=['hls_toolkit', 'cpp_toolkit', 'python_toolkit', 'tcl_toolkit', 'vivado_toolkit', 'vhdl_toolkit' ],
      zip_safe=False)