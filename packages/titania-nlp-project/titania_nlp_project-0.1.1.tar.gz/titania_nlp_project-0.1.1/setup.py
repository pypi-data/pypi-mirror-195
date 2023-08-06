from setuptools import setup

setup(
    name='titania_nlp_project',
    version='0.1.1',
    description='Named Entity Recognition package using SpaCy',
    author='Sai Teja Reddy',
    author_email='saitejareddy123@gmail.com',
    url='https://github.com/your_username/titania_nlp_project',
    packages=['titania_nlp_project'],
    install_requires=[    'spacy>=3.0.0,<4.0.0',   
                         'spacytextblob>=3.0.1',
                         'nltk>=3.6.0',
                         'boto3>=1.17.71,<2.0.0'],
    python_requires='>=3.6, <4',
)

