from setuptools import find_packages, setup

setup(
    name="twitter-async-search",
    version="1.0.3",
    description="Fast twitter search API",
    author="Trevor Hobenshield",
    author_email="trevorhobenshield@gmail.com",
    url="https://github.com/trevorhobenshield/twitter-async-search",
    install_requires=[
        "aiohttp",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        twitter-async-search=src.main:main
    """,
    keywords="twitter search api async",
    packages=find_packages(),
    include_package_data=True,
    package_data={'src': ['config/*', 'log/*']}
)
