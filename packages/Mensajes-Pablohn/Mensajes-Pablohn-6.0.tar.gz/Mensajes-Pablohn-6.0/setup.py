# from struct import pack
from setuptools import setup, find_packages

setup(
    name='Mensajes-Pablohn',
    # name='Mensajes',
    # version='1.0',
    # version='2.0',
    # version='3.0',
    # version='4.0',
    # version='5.0',
    version='6.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pablo Hernández Núñez',
    author_email='hola@p4bl0.dev',
    url='https://www.p4bl0.dev',
    license_files=['LICENSE'],
    # packages=['mensajes', 'mensajes.hola', 'mensajes.adios'],
    packages=find_packages(),
    # scripts=['test.py'],
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() 
                        for paquete in open("requirements.txt").readlines()],
    
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities'
    ],

)