from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Package for visual scripting'
LONG_DESCRIPTION = 'A package for creating simple programs as graphs of nodes for quick prototyping.'

setup(
    name="visualscript",
    version=VERSION,
    author="Wachu (Adam Wachowicz)",
    author_email="<adam.wachowicz@vp.pl>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['visual', 'graph', 'blueprint'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)