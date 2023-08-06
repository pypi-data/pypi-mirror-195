# __Author__ = "Pranav Chandran"
# __Date__ = 05-03-2023
# __Time__ = 12:26
# __FileName__ = setup.py
from setuptools import setup, find_packages

setup(
    name='testing_crypto_1',
    version='0.5',
    description='Crypting code',
    author='Pranav Chandran',
    author_email='pranav.chandran@gmail.com',
    packages=find_packages(),  # same as name if we are not using any subpackages
    install_requires=['pyarmor'],  # from pypi
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

