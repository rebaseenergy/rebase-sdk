from setuptools import setup, find_packages

setup(
    name='rebase',
    url='https://github.com/rebaseenergy/rebase-sdk',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=['requests>=2.20.0', 'pandas>=1.0.0'],
    include_package_data=True,
    version='0.0.1-beta',
    license='MIT',
    description='Rebase Python SDK',
    long_description=open('README.md').read(),
)
