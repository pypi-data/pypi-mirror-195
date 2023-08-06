from setuptools import setup

setup(
    name='aie-secrets',
    version='1.9.9',
    description='My first Python package',
    author='johnson',
    author_email='johnssimon007@email.com',
    packages=['aie_secrets'],
    install_requires=[
        'requests',
        'dnspython',
    ],
        entry_points={
            'console_scripts': [
                'aie-secrets=aie_secrets.__main__:main',
            ],
        },
)
