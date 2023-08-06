from setuptools import setup, find_packages

setup(
    name='shulker',
    version='0.3.9',
    author='PortalHubYT',
    author_email='portalhub.business@gmail.com',
    description='A minecraft interface using RCON',
    url='https://github.com/PortalHubYT/mc_api',
    packages=find_packages(),
    package_data={
        'shulker': ['functions/*.json', 'components/*.json', 'server/*.json']
    },
    install_requires=['docker', 'mctools', 'pillow', 'mcstatus', 'nbtlib==1.12.1'], # add your package dependencies here
)
