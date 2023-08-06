from setuptools import setup


setup(
    name="pychatgpt-cli",
    version="0.0.1",
    install_requires=[
        "click",
        "openai",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "gcli = cli:main",
        ],
    },
)
