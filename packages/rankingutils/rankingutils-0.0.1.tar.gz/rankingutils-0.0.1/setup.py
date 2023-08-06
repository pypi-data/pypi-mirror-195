from setuptools import find_packages, setup
setup(
    name='rankingutils',
    packages=find_packages(include=['rankingutils']),
    install_requires=['pandas==1.5.2', 'elasticsearch==8.4.1', 'requests==2.28.2'],
    version='0.0.1',
    description='Library with ranking utils',
    author='Dasha Zapekina',
    license='MIT',
)