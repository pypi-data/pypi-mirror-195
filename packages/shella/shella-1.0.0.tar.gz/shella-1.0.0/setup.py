from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'An asynchronous Interactive shell'
LONG_DESCRIPTION = 'An asynchronous interactive shell to interact with your program with autocompleting, history and argument validation'

setup(

        name="shella", 
        version=VERSION,
        author="Malte Gruber",
        author_email="<contact@maltegruber.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["aiofiles",],
        
        keywords=['python', 'first package'],
        #https://pypi.org/classifiers/
        classifiers= [
            
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux ",
        ]
)