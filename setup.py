from setuptools import setup, find_packages
from pathlib import Path


project_directory = Path(__file__).parent
long_description = (project_directory / "README.md").read_text()

setup(
    name='ambrogio',
    version='0.1.5',

    description='A simple framework to handle complex scripts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    url='https://github.com/officinaMusci/ambrogio',
    project_urls={
        'Source': 'https://github.com/officinaMusci/ambrogio',
        'Tracker': 'https://github.com/officinaMusci/ambrogio/issues',
    },
    
    author='Danilo Musci',
    author_email='officina@musci.ch',
    
    license='BSD 3-Clause',
    
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['ambrogio = ambrogio.cli:execute']
    },

    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'psutil',
        'inquirer',
        'rich',
        'plotly'
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)