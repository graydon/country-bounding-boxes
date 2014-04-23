from setuptools import setup

setup(
    name='country-bounding-boxes',
    version='0.1',
    description='Library of bounding boxes of countries (and associated data)',
    long_description=open('README.rst').read(),
    author='Graydon Hoare',
    author_email='graydon@mozilla.com',
    license='BSD',
    url='https://github.com/graydon/country-bounding-boxes',
    include_package_data=True,
    packages=['country_bounding_boxes'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ]
)
