from setuptools import setup, find_packages

setup(
    name='newspapers3k_scraper',
    version='1.0.0',
    description='Multi-threaded, super fast scraper with newspapers3k',
    author='Aayush',
    author_email='ltsaayushk193@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3'
    ]
)