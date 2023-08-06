from setuptools import setup, find_packages

setup(
  name="fsapi-tools",
  version="0.3.0",
  description="Frontier Silicon (former Frontier Smart) API",
  url="https://github.com/MatrixEditor/frontier-smart-api",
  author="MatrixEditor",
  author_email="not@supported.com",
  license="MIT License",

  packages=find_packages(
    where='.',
    include=['fsapi*']
  ),

  requires=['urllib3', 'xml'],

  classifiers= [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ]
)

