from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Nadya Nupreichik',
    author_email='nady2505429@gmail.com',
    description='Pure-python command-line calculator.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.pycalc:main',
        ],
    }
)
