from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='brzcode',
    version='1.0.7',
    license='MIT License',
    author='Gustavo Martinez',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='gamezinhoo@outlook.com',
    keywords='brzcode',
    description=u'Uma programação simples, completa, e veloz.',
    packages=['brzcode'],
    install_requires=['colorama'],)