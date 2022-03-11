from distutils.core import setup

NAME = "lispress_to_graph_program"

setup(
    name=NAME,
    version="0.0.1",
    author="Eli Whitehouse",
    author_email="eli.whitehouse@aizwei.com",
    description="conversion of lispress to dataset for graph program learning",
    packages=[NAME],
    package_data={NAME: ['lispress_to_graph_program.so']})