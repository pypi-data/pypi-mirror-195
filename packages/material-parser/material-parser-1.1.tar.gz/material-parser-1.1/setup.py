from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

#import unittest


#def my_test_suite():
#    test_loader = unittest.TestLoader()
#    test_suite = test_loader.discover('nerd/tests', pattern='test_*.py')
#    return test_suite


setup(
    name='material-parser',
    version='1.1',
    description='Grobid superconductors tools material parser',
    url='https://github.com/lfoppiano/grobid-superconductors-tools',
    author='Luca Foppiano',
    author_email='FOPPIANO.Luca@nims.go.jp',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # 'Topic :: Text processing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['text mining', 'machine learning'],
    install_requires=['pymatgen==2021.3.3'],
    # package_dir={'commons': ''},
    # packages={'commons'},
    zip_safe=False#,
    #test_suite='setup.my_test_suite'
)