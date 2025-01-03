from setuptools import setup, find_packages

setup(
    name='privateGPT_server',
    version='1.0.0',
    description='PrivateGPT server for OPA queries',
    author='Tanmoy Dutta',
    author_email='duttatanmoy834@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.0.3',  # or whatever version you require
        # Add any other dependencies your Flask app needs
        # Example: 'requests', 'sqlalchemy', etc.
    ],
    entry_points={
        'console_scripts': [
            'privateGPT_server_run=privateGPT_server.run:main',
        ],
    },
)
