from setuptools import setup

py_modules = [
    'requests',
    'bs4',
    'xdg'
]

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='boj-tool',
      version='v1.0.0',
      description='A tool for submitting to BOJ',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ryang Sohn',
      author_email='loop.infinitely@gmail.com',
      install_requirements=py_modules,
      entry_points={
          'console_scripts': [
              'boj=boj_tool:main'
          ]
      },
      project_urls={
          'Bug Reports': 'https://github.com/sohnryang/boj-tool/issues',
          'Source': 'https://github.com/sohnryang/boj-tool'
      })
