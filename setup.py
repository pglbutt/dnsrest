try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dnsrest',
    version='0.0.1',
    description='Like flask but over dns',
    author='Paul Glass',
    author_email='pnglass@gmail.com',
    packages=['dnsrest'],
    package_dir={'dnsrest': 'dnsrest'},
    keywords=['dnsrest'],
    install_requires=[
        'dnspython',
    ],
)
