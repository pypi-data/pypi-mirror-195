from setuptools import setup, find_packages

setup( 
     
name='Mensajes-Wilmar',
version='4.0',  
description='Paquete que muestra mensajes de saludos y despedidas',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
author='Wilmar Galvis', 
author_email='wagalvis24@gmail.com',
url='https://www.instagram.com/wilmargalvis/', 
license_files=['LICENSE'],  
packages=find_packages(),
#packages=['mensajes','mensajes.hola','mensajes.adios'],
#scripts=['test.py'],
scripts=[],
test_suite='tests',
install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()], 
classifiers=[ 
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Utilities'
    ]  
 
)

