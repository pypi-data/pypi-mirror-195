from setuptools import setup, find_packages

setup(
    name='colorsgradient',
    version='15',
    author='Peter Waller (Thanks to Christopher Jones and Stefano Rivera)',
    author_email='p@pwaller.net',
    description='Pure-python Colors implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pwaller/pyfiglet',
    packages=find_packages(),
    install_requires=[
        'requests','colorama'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
