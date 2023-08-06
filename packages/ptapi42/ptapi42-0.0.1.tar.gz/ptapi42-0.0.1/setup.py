from setuptools import setup


setup(
    name="ptapi42",
    version="0.0.1",
    author="42 Portugal",
    author_email="root@42porto.com",
    description="A python package that simplifies the process of making API requests to 42's API.",
    long_description_content_type="text/markdown",
    url="https://github.com/42-Portugal/ptapi42",
    project_urls={
        "Bug Tracker": "https://github.com/42-Portugal/ptapi42/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=['ptapi42'],
    python_requires=">=3.10",
    install_requires=["requests"]
)
