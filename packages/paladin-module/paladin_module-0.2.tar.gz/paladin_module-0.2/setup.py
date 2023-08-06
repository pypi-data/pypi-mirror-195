from setuptools import setup
from setuptools import find_packages

setup(
    name='paladin_module',
    version='0.2',
    description='Just module for practice. Check out my git hub',
    url='https://github.com/paladinxb',
    author='Ilya Kharkovec',
    author_email='paladinxb@gmail.com',
    py_modules=['paladin_module'],
    #packages=['my_module'],
    packages=find_packages(),
    install_requires=[
        # 0 requries
    ],
)