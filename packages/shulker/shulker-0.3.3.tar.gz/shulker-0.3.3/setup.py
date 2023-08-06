from setuptools import setup, find_packages

setup(
    name='shulker',
    version='0.3.3',
    author='PortalHubYT',
    author_email='portalhub.business@gmail.com',
    description='A minecraft interface using RCON',
    url='https://github.com/PortalHubYT/mc_api',
    packages=find_packages(),
    install_requires=['docker', 'mctools', 'pillow', 'mcstatus'], # add your package dependencies here
)
