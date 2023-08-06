from setuptools import setup

setup(
    name='NWSh',
    version='0.1.2',
    packages=['NWSh'],
    url='https://www.nwsoft.tk',
    license='GPL',
    author='ZCG-Coder',
    author_email='andy@nwsoft.tk',
    description='A little library for the NWSh development',
    install_requires=[
        'prompt_toolkit',
        'json5rw',
    ],
    data_files=[('NWSh/resources', ['NWSh/resources/settings.json'])],
    include_dirs=['NWSh/resources'],
    include_package_data=True,
)
