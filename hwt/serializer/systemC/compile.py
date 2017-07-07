from setuptools.extension import Extension
from setuptools.dist import Distribution
from setuptools.command.build_ext import build_ext


class SystemCMake():
    
    def test(self, name, srcs):
        module1 = Extension('test',
                    libraries=['systemc', "pthread"],
                    extra_compile_args=["-O3", "-Wall"],
                    sources=['sample.cpp'])

        dist = Distribution(dict(name="sample",
                                 ext_modules=[module1]))
        cmd = build_ext(dist)
        cmd.initialize_options()
        cmd.finalize_options()
        # cmd.build_extension(module1)
        cmd.run()
        
        print("end")

if __name__ == "__main__":
    m = SystemCMake()
    srcs = ["sample.cpp"]
    m.test("test", srcs)
