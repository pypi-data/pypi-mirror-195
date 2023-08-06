from setuptools import *

with open("README.md", "r") as arq:
    long_desc = arq.read()

setup(
    name="valorantheadhunterapipy", # Replace with your own username
    version="1.1.2",
    author="OnlyTH",
    description="Somente testes",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/OnlyTH777/VALORANT-Headhunter.py",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["valclient", "requests", "urllib3"],
    license = 'MIT License'
)