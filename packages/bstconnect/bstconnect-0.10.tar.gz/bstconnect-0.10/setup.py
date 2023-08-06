from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Connects to all BlueStacks devices that use Hyper-V (dynamic port!) via ADB and returns a DataFrame"

# Setting up
setup(
    name="bstconnect",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/bstconnect',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_bstcfg2df', 'a_pandas_ex_regex_enhancements', 'capture_stdout_decorator', 'flexible_partial', 'kthread', 'kthread_sleep', 'pandas', 'psutil'],
    keywords=['bluestacks', 'adb', 'android'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_bstcfg2df', 'a_pandas_ex_regex_enhancements', 'capture_stdout_decorator', 'flexible_partial', 'kthread', 'kthread_sleep', 'pandas', 'psutil'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*