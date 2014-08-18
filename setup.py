from setuptools import setup

setup(
    name='country-bounding-boxes',
    version='0.2.2',
    description='Library of bounding boxes of countries (and associated data)',
    long_description=open('README.rst').read(),
    author='Graydon Hoare',
    author_email='graydon@pobox.com',
    license='LICENSE.txt',
    url='https://github.com/graydon/country-bounding-boxes',
    include_package_data=True,
    packages=['country_bounding_boxes'],
    install_requires=['iso3166'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Internationalization',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
