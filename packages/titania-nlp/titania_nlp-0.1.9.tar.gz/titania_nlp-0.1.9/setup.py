from setuptools import setup

setup(
    name='titania_nlp',
    version='0.1.9',
    description='Named Entity Recognition package using SpaCy',
    author='Sai Teja Reddy',
    author_email='saitejareddy123@gmail.com',
    url='https://github.com/your_username/titania_nlp',
    packages=['titania_nlp'],
    install_requires=[    'spacy>=3.0.0,<4.0.0',    'spacytextblob>=3.0.1'],
    python_requires='>=3.6, <4',
)
