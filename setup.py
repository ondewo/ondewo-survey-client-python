from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='ondewo-survey-client',
    version='2.0.0',
    author='Ondewo GmbH',
    author_email='info@ondewo.com',
    description='This library facilitates the interaction between a user and his/her Survey server.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ondewo/ondewo-survey-client-python',
    packages=[
        np
        for np in filter(
            lambda n: n.startswith('ondewo.') or n == 'ondewo',
            find_packages()
        )
    ],
    include_package_data=True,
    package_data={
        'ondewo.nlu': ['py.typed', '*.pyi'],
        'ondewo.survey': ['py.typed', '*.pyi'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3',
    install_requires=requires,
)
