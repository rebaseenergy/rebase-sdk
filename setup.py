from setuptools import setup, find_packages

setup(
    name='rebase-toolkit',
    url='https://github.com/rebaseenergy/rebase-sdk',
    packages=find_packages(exclude=["*tests*", "*debug*","*docs*"]),
    install_requires=['requests>=2.20.0', 'pandas>=1.0.0', 'dill'],
    include_package_data=True,
    version='0.0.4-beta',
    license='Apache 2.0',
    description='Rebase Python toolkit',
    long_description=open('README.md').read(),
)
