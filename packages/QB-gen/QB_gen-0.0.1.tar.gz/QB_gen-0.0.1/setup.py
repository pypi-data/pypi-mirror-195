from setuptools import setup, find_packages

setup(
    name="QB_gen",
    version="0.0.1",
    author="Ngo Hong Quoc Bao",
    author_email="quocbao.ngoh@gmail.com",
    description="Password validator and generator CLI tool.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NgoQuocBao1010/QB-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.9",
    install_requires=["typer==0.7.0", "rich==12.6.0", "Unidecode==1.3.6"],
)
