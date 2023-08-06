from setuptools import setup, find_packages

setup(
    name='jionlp-time',
    packages=find_packages(exclude=['local_tests']),
    version='1.0.0',
    install_requires=[],
    # extras_require={
    # },
    author='cone387',
    maintainer_email='1183008540@qq.com',
    license='MIT',
    url='https://github.com/cone387/JioNLPTimeParser',
    python_requires='>=3.7, <4',
)