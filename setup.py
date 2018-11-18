import setuptools

from setuptools import setup
from os import path

py_modules = [
    'requests',
    'bs4',
    'xdg'
]

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='boj-tool',
      version='1.1.0',
      description='A tool for submitting to BOJ',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ryang Sohn',
      author_email='loop.infinitely@gmail.com',
      install_requires=py_modules,
      entry_points={
          'console_scripts': [
              'boj=boj:main'
          ]
      },
      packages=setuptools.find_packages(),
      project_urls={
          'Bug Reports': 'https://github.com/sohnryang/boj-tool/issues',
          'Source': 'https://github.com/sohnryang/boj-tool'
      })
