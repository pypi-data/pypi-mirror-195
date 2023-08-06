from setuptools import setup, find_packages
setup(
    name = 'lftk',  
    version='1.0-beta-2',
    license='CC BY-NC 4.0',   
    description = 'Comprehensive Multilingual Linguistic Features Extraction in Python',
    author = 'Bruce W. Lee',
    author_email = 'brucelws@seas.upenn.edu', 
    packages=find_packages('lftk'),
    package_dir={'': 'lftk'},
    url='https://github.com/brucewlee/lftk',
    keywords='linguistic feature',
    install_requires=[
          'pandas',
          'ndjson',
          'spacy'
      ],

)